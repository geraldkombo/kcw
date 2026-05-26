"""Land Intelligence Agent — analyses land suitability, soil health, idle detection,
yield prediction, and contract-farm matching using NASA POWER satellite data."""

from typing import Optional
from agriculture_intelligence.land_intelligence import LandIntelligence
from agriculture_intelligence.market_intelligence import MarketIntelligence
from satellite.power_client import PowerClient


class LandIntelligenceAgent:
    """Analyses agricultural land for investment-grade intelligence."""

    def __init__(self, power: Optional[PowerClient] = None):
        self.power = power or PowerClient()
        self.land = LandIntelligence(self.power)
        self.market = MarketIntelligence(self.power)

    async def analyse(self, farmer_profile: dict) -> dict:
        lat = farmer_profile.get("latitude", 0.0)
        lon = farmer_profile.get("longitude", 0.0)
        county = farmer_profile.get("county", "")
        farm_size = farmer_profile.get("farm_size_ha", 1.0)
        crop = farmer_profile.get("primary_crop", "maize")

        suitability = await self.land.analyse_land_suitability(lat, lon, county, farm_size)
        idle = await self.land.detect_idle_land_risk(lat, lon)
        yield_est = await self.land.estimate_yield(lat, lon, crop, farm_size)

        contracts = []
        for c in [crop, suitability.get("best_crop", "")]:
            if c:
                found = await self.market.find_contract_farming(county, c, farm_size)
                contracts.extend(found)

        return {
            "farm_size_ha": farm_size,
            "county": county,
            "land_suitability": suitability,
            "idle_land_risk": idle,
            "yield_projection": yield_est,
            "contract_farming_options": contracts,
            "data_source": "nasa_power",
        }
