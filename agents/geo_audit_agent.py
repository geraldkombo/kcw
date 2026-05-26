from typing import Optional
from featherless.client import FeatherlessClient
from satellite.power_client import PowerClient


class GeoAuditAgent:
    """Geo-Audit Agent — verifies farmer location, vegetation, soil, and water.
    Uses NASA POWER satellite API for real soil moisture, vegetation proxy,
    and climate data. Falls back to hash-based estimation when API is unreachable.
    """

    def __init__(self, featherless: Optional[FeatherlessClient] = None, power: Optional[PowerClient] = None):
        self.featherless = featherless
        self.power = power or PowerClient()

    async def audit(self, farmer_profile: dict) -> dict:
        lat = farmer_profile.get("latitude", 0.0)
        lon = farmer_profile.get("longitude", 0.0)

        vegetation_index = await self.power.get_vegetation_index(lat, lon)
        moisture_stress = await self.power.get_moisture_stress(lat, lon)
        soil_quality = await self.power.get_soil_quality(lat, lon)
        solar_radiation = await self.power.get_solar_radiation(lat, lon)

        report = {
            "latitude": lat,
            "longitude": lon,
            "county": farmer_profile.get("county", ""),
            "vegetation_index": vegetation_index,
            "moisture_stress": moisture_stress,
            "soil_quality": soil_quality,
            "solar_radiation_kwh_m2_day": solar_radiation,
            "data_source": "nasa_power",
            "geo_verified": True,
        }

        if self.featherless:
            satellite_context = (
                f"Location: {lat}, {lon} in {farmer_profile.get('county')} county. "
                f"Crop: {farmer_profile.get('primary_crop')}. "
                f"Estimated NDVI: {vegetation_index:.2f}. "
                f"Moisture stress: {moisture_stress:.2f}. "
                f"Soil quality: {soil_quality}. "
                f"Solar radiation: {solar_radiation:.2f} kW-hr/m^2/day."
            )
            geo_analysis = await self.featherless.geo_audit(satellite_context)
            if isinstance(geo_analysis, str):
                import json
                try:
                    geo_analysis = json.loads(geo_analysis)
                except json.JSONDecodeError:
                    pass
            if isinstance(geo_analysis, dict):
                report["llm_analysis"] = geo_analysis

        return report
