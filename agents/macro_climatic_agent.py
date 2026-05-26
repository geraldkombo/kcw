from typing import Optional
from satellite.power_client import PowerClient


class MacroClimaticAgent:
    """Macro-Climatic Agent — overlays real NASA POWER satellite climate data
    on farmer location. Sources: MERRA-2 reanalysis (temp, precip, soil moisture)
    and SRB radiation (solar). Falls back to county-level heuristics when API
    is unreachable.
    """

    def __init__(self, power: Optional[PowerClient] = None):
        self.power = power or PowerClient()

    async def assess(self, farmer_profile: dict) -> dict:
        lat = farmer_profile.get("latitude", 0.0)
        lon = farmer_profile.get("longitude", 0.0)
        county = farmer_profile.get("county", "")

        # Real NASA POWER data
        temp = await self.power.get_temperature(lat, lon)
        precip = await self.power.get_precipitation(lat, lon)
        solar = await self.power.get_solar_radiation(lat, lon)

        drought_risk = self._compute_drought_risk(precip, temp.get("mean", 25.0), solar, county)
        temp_anomaly = round(temp.get("mean", 25.0) - 25.0, 2)
        rainfall_z_score = round((precip - 3.0) / 2.0, 2)

        return {
            "drought_risk": round(drought_risk, 4),
            "temp_anomaly": temp_anomaly,
            "rainfall_z_score": rainfall_z_score,
            "precip_mm_day": precip,
            "temp_mean_c": temp.get("mean", 25.0),
            "temp_max_c": temp.get("max", 32.0),
            "temp_min_c": temp.get("min", 18.0),
            "solar_radiation_kwh_m2_day": solar,
            "data_source": "nasa_power",
            "climate_zone": self._classify_zone(lat, lon, county, precip, temp.get("mean", 25.0)),
            "advisory": self._generate_advisory(county, drought_risk, precip, temp.get("mean", 25.0)),
        }

    def _compute_drought_risk(self, precip: float, temp: float, solar: float, county: str) -> float:
        drought_prone_counties = {"Machakos", "Kilifi", "Homa Bay", "Nakuru"}
        # Base risk from real NASA POWER precipitation (mm/day)
        # Equatorial Kenya: <2mm is drought, >8mm is high rainfall
        if precip < 1.0:
            base = 0.8
        elif precip < 2.5:
            base = 0.6
        elif precip < 5.0:
            base = 0.35
        elif precip < 8.0:
            base = 0.15
        else:
            base = 0.05
        # Temperature and solar amplify
        if temp > 30:
            base += 0.15
        elif temp > 27:
            base += 0.05
        if solar > 7.0:
            base += 0.1
        elif solar > 5.5:
            base += 0.05
        # County override for known drought zones
        if county in drought_prone_counties:
            base = max(base, 0.5)
        return min(1.0, base)

    def _classify_zone(self, lat: float, lon: float, county: str, precip: float, temp: float) -> str:
        if county in {"Kisumu", "Homa Bay"}:
            return "lake_basin"
        if county in {"Machakos", "Kilifi"}:
            return "arid_semi_arid"
        if county in {"Meru", "Nyeri", "Kiambu"}:
            return "highland"
        if county in {"Uasin Gishu", "Nakuru"}:
            return "rift_valley"
        if precip < 2.0 and temp > 28:
            return "arid_semi_arid"
        if precip > 8.0:
            return "humid"
        return "transitional"

    def _generate_advisory(self, county: str, drought_risk: float, precip: float, temp: float) -> str:
        if drought_risk > 0.5:
            return (
                f"High drought risk in {county} (precip: {precip:.1f}mm/day, "
                f"temp: {temp:.1f}°C). "
                "Consider drought-resistant seed varieties and irrigation financing."
            )
        if precip < 2.0:
            return (
                f"Below-average rainfall in {county} ({precip:.1f}mm/day). "
                "Monitor soil moisture; supplemental irrigation recommended."
            )
        return (
            f"Standard conditions in {county} ({precip:.1f}mm/day, {temp:.1f}°C). "
            "Proceed with normal credit terms."
        )
