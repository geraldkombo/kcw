from satellite.power_client import PowerClient


class GeoAuditAgent:
    """Geo-Audit Agent — verifies location, vegetation, soil, and water.
    Uses NASA POWER satellite API for real soil moisture, vegetation proxy,
    and climate data.
    """

    def __init__(self, power: PowerClient | None = None):
        self.power = power or PowerClient()

    async def audit(self, location: dict) -> dict:
        lat = location.get("latitude", 0.0)
        lon = location.get("longitude", 0.0)

        return {
            "latitude": lat,
            "longitude": lon,
            "vegetation_index": await self.power.get_vegetation_index(lat, lon),
            "moisture_stress": await self.power.get_moisture_stress(lat, lon),
            "soil_quality": await self.power.get_soil_quality(lat, lon),
            "solar_radiation_kwh_m2_day": await self.power.get_solar_radiation(lat, lon),
            "data_source": "nasa_power",
        }
