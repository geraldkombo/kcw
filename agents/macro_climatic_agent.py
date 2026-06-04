from typing import Optional
from satellite.power_client import PowerClient
from knowledge.traditional_foods import TraditionalFoodsIndex


class MacroClimaticAgent:
    """Macro-Climatic Agent — overlays real NASA POWER satellite climate data
    on farmer location. Sources: MERRA-2 reanalysis (temp, precip, soil moisture)
    and SRB radiation (solar). Falls back to county-level heuristics when API
    is unreachable.

    Enhanced with Patrick Maundu's traditional food plants knowledge:
    - Crop origin classification (indigenous vs exotic)
    - Traditional intercropping patterns
    - Ethnic food demand corridors
    - Nutritional context for crop recommendations
    """

    def __init__(self, power: Optional[PowerClient] = None):
        self.power = power or PowerClient()
        self.traditional_foods = TraditionalFoodsIndex()

    async def assess(self, farmer_profile: dict) -> dict:
        lat = farmer_profile.get("latitude", 0.0)
        lon = farmer_profile.get("longitude", 0.0)
        county = farmer_profile.get("county", "")
        crop = farmer_profile.get("primary_crop", "")

        # Real NASA POWER data
        temp = await self.power.get_temperature(lat, lon)
        precip = await self.power.get_precipitation(lat, lon)
        solar = await self.power.get_solar_radiation(lat, lon)

        drought_risk = self._compute_drought_risk(precip, temp.get("mean", 25.0), solar, county)
        temp_anomaly = round(temp.get("mean", 25.0) - 25.0, 2)
        rainfall_z_score = round((precip - 3.0) / 2.0, 2)

        # Traditional food plants context (Maundu, 1999)
        tf_crops = self.traditional_foods.get_crops_for_region(county)
        tf_classified = self.traditional_foods.classify_crop(crop) if crop else None
        tf_patterns = self.traditional_foods.get_intercropping_patterns(county)
        tf_corridors = self.traditional_foods.get_food_corridors(county)

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
            "advisory": self._generate_advisory(county, drought_risk, precip, temp.get("mean", 25.0), tf_classified, tf_corridors),
            "traditional_foods": {
                "crop_origin": (tf_classified.get("status") if tf_classified else None),
                "crop_classification": (f"{tf_classified.get('status', 'unknown')} — {tf_classified.get('origin', '')}" if tf_classified else None),
                "traditional_crops_in_county": len(tf_crops),
                "indigenous_crops": [c["name_sw"].split("/")[0].strip() for c in tf_crops if c.get("status") == "indigenous"],
                "intercropping_patterns": tf_patterns,
                "market_demand_corridors": tf_corridors,
            } if tf_crops else {},
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

    def _generate_advisory(self, county: str, drought_risk: float, precip: float, temp: float,
                           tf_classified: dict | None = None,
                           tf_corridors: list | None = None) -> str:
        parts = []
        if drought_risk > 0.5:
            parts.append(
                f"High drought risk in {county} (precip: {precip:.1f}mm/day, "
                f"temp: {temp:.1f}°C). "
                "Consider drought-resistant seed varieties and irrigation financing."
            )
        elif precip < 2.0:
            parts.append(
                f"Below-average rainfall in {county} ({precip:.1f}mm/day). "
                "Monitor soil moisture; supplemental irrigation recommended."
            )
        else:
            parts.append(
                f"Standard conditions in {county} ({precip:.1f}mm/day, {temp:.1f}°C). "
            )

        # Traditional foods context (Maundu, 1999)
        if tf_classified:
            status = tf_classified.get("status", "")
            origin = tf_classified.get("origin", "")
            if status == "indigenous":
                parts.append(
                    f"Crop is indigenous to East Africa ({origin}). "
                    "Naturally adapted to local conditions — lower input requirements."
                )
            elif status == "naturalised":
                parts.append(
                    f"Crop is naturalised in East Africa ({origin}). "
                    "Well-adapted; traditional varieties may outperform modern hybrids."
                )
            elif status == "exotic":
                parts.append(
                    f"Crop is exotic to East Africa ({origin}). "
                    "Higher input requirements for water and fertiliser."
                )

        if tf_corridors:
            corridors = ", ".join(c["name"] for c in tf_corridors)
            parts.append(
                f"Ethnic food demand corridors from {county}: {corridors}. "
                "Traditional varieties have established market channels."
            )

        return " ".join(parts)
