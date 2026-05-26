"""AI Agriculture Investment Advisor Agent — autonomous investment recommendations.
This is the system that makes AI-driven agriculture investments, not just an app."""

from typing import Optional
from agriculture_intelligence.investment_advisor import InvestmentAdvisor
from satellite.power_client import PowerClient


class InvestmentAdvisorAgent:
    """Autonomous agriculture investment advisor. Combines land, water, solar,
    seed, market, and cooperative intelligence to recommend optimal investments."""

    def __init__(self, power: Optional[PowerClient] = None):
        self.power = power or PowerClient()
        self.advisor = InvestmentAdvisor(self.power)

    async def recommend(self, farmer_profile: dict) -> dict:
        lat = farmer_profile.get("latitude", 0.0)
        lon = farmer_profile.get("longitude", 0.0)
        county = farmer_profile.get("county", "")
        farm_size = farmer_profile.get("farm_size_ha", 1.0)
        budget = farmer_profile.get("budget_kes", 500000)
        crop = farmer_profile.get("primary_crop", "maize")
        coop_members = farmer_profile.get("cooperative_members", 0)
        dairy_cows = farmer_profile.get("dairy_cows", 0)

        recommendations = await self.advisor.recommend_investments(
            latitude=lat, longitude=lon, county=county,
            farm_size_ha=farm_size, budget_kes=budget,
            crop=crop, cooperative_members=coop_members,
            dairy_cows=dairy_cows,
        )

        portfolio = None
        if budget >= 200000:
            portfolio = await self.advisor.get_portfolio_diversification(lat, lon, budget)

        return {
            "farmer_id": farmer_profile.get("id"),
            "county": county,
            "farm_size_ha": farm_size,
            "budget_kes": budget,
            "recommendations": recommendations,
            "portfolio": portfolio,
            "investment_readiness": self._score_readiness(farmer_profile),
        }

    def _score_readiness(self, profile: dict) -> dict:
        score = 0
        if profile.get("farm_size_ha", 0) >= 1:
            score += 20
        if profile.get("chama_member"):
            score += 15
        if profile.get("sacco_member"):
            score += 15
        if profile.get("mpesa_monthly_velocity", 0) >= 5000:
            score += 10
        if profile.get("latitude", 0) != 0:
            score += 20
        if profile.get("primary_crop"):
            score += 10
        if profile.get("dairy_cows", 0) > 0:
            score += 10

        return {
            "score": score,
            "level": "high" if score >= 70 else "medium" if score >= 40 else "low",
            "missing": [] if score >= 70 else (
                ["farm details"] if score < 40 else []
            ),
        }
