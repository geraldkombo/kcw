"""Cooperative Agent — solves mismanagement of cooperatives: milk, feeds, governance."""

from typing import Optional
from agriculture_intelligence.cooperative_manager import CooperativeManager
from agriculture_intelligence.market_intelligence import MarketIntelligence


class CooperativeAgent:
    """Manages cooperative performance: milk pricing, feed procurement, governance."""

    def __init__(self):
        self.coop = CooperativeManager()
        self.market = MarketIntelligence()

    async def assess(self, cooperative_data: dict) -> dict:
        members = cooperative_data.get("members", 0)
        milk_price = cooperative_data.get("avg_milk_price_kes", 45)
        feed_cost = cooperative_data.get("avg_feed_cost_kes", 42)
        default_rate = cooperative_data.get("default_rate_pct", 8)
        volume_litres = cooperative_data.get("daily_volume_litres", 0)
        dairy_cows = cooperative_data.get("dairy_cows", 2)

        health = await self.coop.assess_cooperative_health(members, milk_price, feed_cost, default_rate)
        milk_opt = await self.coop.optimize_milk_pricing(milk_price, volume_litres)
        feed_opt = await self.coop.optimize_feed_procurement(members, dairy_cows)
        governance = await self.coop.get_governance_recommendations(health.get("health_score", 50), members)

        return {
            "cooperative_health": health,
            "milk_pricing_optimization": milk_opt,
            "feed_procurement_optimization": feed_opt,
            "governance_recommendations": governance,
            "total_annual_gain_kes": milk_opt.get("estimated_annual_gain_kes", 0) + feed_opt.get("annual_savings_kes", 0),
        }
