"""Market Intelligence Agent — finds best prices, contract farming, and input optimisation."""

from typing import Optional
from agriculture_intelligence.market_intelligence import MarketIntelligence
from agriculture_intelligence.water_optimizer import WaterOptimizer
from agriculture_intelligence.land_intelligence import LandIntelligence
from satellite.power_client import PowerClient


class MarketIntelligenceAgent:
    """Provides real-time market intelligence for agricultural investments."""

    def __init__(self, power: Optional[PowerClient] = None):
        self.power = power or PowerClient()
        self.market = MarketIntelligence(self.power)
        self.water = WaterOptimizer(self.power)
        self.land = LandIntelligence(self.power)

    async def analyse(self, farmer_profile: dict) -> dict:
        lat = farmer_profile.get("latitude", 0.0)
        lon = farmer_profile.get("longitude", 0.0)
        county = farmer_profile.get("county", "")
        farm_size = farmer_profile.get("farm_size_ha", 1.0)
        crop = farmer_profile.get("primary_crop", "maize")
        dairy_cows = farmer_profile.get("dairy_cows", 0)

        # Best price for their crop
        yield_est = await self.land.estimate_yield(lat, lon, crop, farm_size)
        price_info = await self.market.get_best_price(crop, yield_est.get("total_yield_tonnes", 1))

        # Contract farming
        contracts = await self.market.find_contract_farming(county, crop, farm_size)

        # Feed prices if dairy
        feed_info = None
        if dairy_cows > 0:
            feed_info = await self.market.get_best_feed_price(dairy_cows)

        # Idle land opportunity
        idle_opp = await self.market.get_idle_land_opportunity(lat, lon, farm_size)

        return {
            "crop": crop,
            "quantity_tonnes": yield_est.get("total_yield_tonnes", 1),
            "market_price": price_info,
            "contract_farming": contracts,
            "feed_optimization": feed_info,
            "idle_land_opportunity": idle_opp,
            "data_source": "nasa_power",
        }
