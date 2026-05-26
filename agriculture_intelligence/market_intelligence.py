"""Market intelligence — best-price routing, contract farming matching, idle land marketplace,
and input supplier optimization. Turns agriculture into an investable asset class."""

import math
from typing import Any

from satellite.power_client import PowerClient


class MarketIntelligence:
    """Finds best prices, matches contract farming opportunities, and optimises input sourcing."""

    # Reference market prices (KES/tonne) — in production, these come from live APIs
    MARKET_PRICES = {
        "maize": {"current": 45000, "high_30d": 52000, "low_30d": 38000, "trend": "stable"},
        "beans": {"current": 85000, "high_30d": 95000, "low_30d": 72000, "trend": "up"},
        "tea": {"current": 200000, "high_30d": 220000, "low_30d": 180000, "trend": "stable"},
        "coffee": {"current": 350000, "high_30d": 400000, "low_30d": 300000, "trend": "up"},
        "wheat": {"current": 40000, "high_30d": 45000, "low_30d": 35000, "trend": "down"},
        "sunflower": {"current": 60000, "high_30d": 70000, "low_30d": 50000, "trend": "up"},
        "milk_per_litre": {"current": 52, "high_30d": 58, "low_30d": 45, "trend": "stable"},
        "drought_resistant_seed": {"current": 80000, "high_30d": 90000, "low_30d": 65000, "trend": "up"},
    }

    # Contract farming offers (marketplace)
    CONTRACT_FARMING_OFFERS = [
        {
            "id": "CF-001",
            "crop": "maize",
            "buyer": "Unga Limited",
            "price_kes_per_tonne": 48000,
            "min_tonnes": 5,
            "duration_months": 12,
            "requirements": "Certified seed, good agricultural practices, delivery to Nakuru depot",
        },
        {
            "id": "CF-002",
            "crop": "beans",
            "buyer": "Kenya Nut Company",
            "price_kes_per_tonne": 92000,
            "min_tonnes": 2,
            "duration_months": 6,
            "requirements": "Rosecoco variety, moisture content <13%, Thika delivery",
        },
        {
            "id": "CF-003",
            "crop": "tea",
            "buyer": "KTDA",
            "price_kes_per_tonne": 210000,
            "min_tonnes": 1,
            "duration_months": 24,
            "requirements": "Registered tea grower, KTDA factory catchment area",
        },
        {
            "id": "CF-004",
            "crop": "drought_resistant_seed",
            "buyer": "Kenya Seed Company",
            "price_kes_per_tonne": 90000,
            "min_tonnes": 3,
            "duration_months": 12,
            "requirements": "Certified drought-resistant varieties, Kitale delivery",
        },
        {
            "id": "CF-005",
            "crop": "sunflower",
            "buyer": "Bidco Africa",
            "price_kes_per_tonne": 65000,
            "min_tonnes": 10,
            "duration_months": 12,
            "requirements": "High-oleic variety, moisture <10%, Thika delivery",
        },
    ]

    # Animal feed suppliers
    ANIMAL_FEED_SUPPLIERS = [
        {"name": "Malinda Feeds", "price_kes_per_kg": 38, "quality_score": 8.5, "location": "Nakuru", "dairy_meal_kes_kg": 42},
        {"name": "Unga Farm Care", "price_kes_per_kg": 42, "quality_score": 9.0, "location": "Nairobi", "dairy_meal_kes_kg": 46},
        {"name": "Sigma Feeds", "price_kes_per_kg": 35, "quality_score": 7.5, "location": "Thika", "dairy_meal_kes_kg": 39},
        {"name": "New KCC Feed", "price_kes_per_kg": 40, "quality_score": 8.0, "location": "Kisumu", "dairy_meal_kes_kg": 44},
    ]

    def __init__(self, power: PowerClient | None = None):
        self.power = power or PowerClient()

    async def get_best_price(self, crop: str, quantity_tonnes: float) -> dict:
        """Find the best market price for a crop, with price projections."""
        price_data = self.MARKET_PRICES.get(crop)
        if not price_data:
            return {"error": f"No price data for {crop}"}

        # Estimated revenue at current price
        revenue = price_data["current"] * quantity_tonnes
        revenue_at_high = price_data["high_30d"] * quantity_tonnes
        upside = ((price_data["high_30d"] / price_data["current"]) - 1) * 100

        # Contract farming premium
        best_contract = None
        best_contract_premium = 0
        for offer in self.CONTRACT_FARMING_OFFERS:
            if offer["crop"] == crop and quantity_tonnes >= offer["min_tonnes"]:
                premium = ((offer["price_kes_per_tonne"] / price_data["current"]) - 1) * 100
                if premium > best_contract_premium:
                    best_contract_premium = premium
                    best_contract = offer

        return {
            "crop": crop,
            "quantity_tonnes": quantity_tonnes,
            "current_price_kes_tonne": price_data["current"],
            "high_30d_price_kes_tonne": price_data["high_30d"],
            "low_30d_price_kes_tonne": price_data["low_30d"],
            "trend": price_data["trend"],
            "estimated_revenue_kes": round(revenue),
            "estimated_revenue_at_high_kes": round(revenue_at_high),
            "upside_potential_pct": round(upside, 1),
            "best_contract_farming": best_contract,
            "contract_farming_premium_pct": round(best_contract_premium, 1) if best_contract else 0,
            "recommendation": (
                f"Sell now at KES {price_data['current']:,}/tonne for KES {revenue:,.0f}. "
                f"Consider contract farming ({best_contract['buyer']}) at KES {best_contract['price_kes_per_tonne']:,}/tonne "
                f"({best_contract_premium:.0f}% premium) if available."
                if best_contract
                else f"Current spot price KES {price_data['current']:,}/tonne. {price_data['trend'].upper()} trend. "
                f"Estimated revenue KES {revenue:,.0f}."
            ),
        }

    async def find_contract_farming(self, county: str, crop: str, farm_size_ha: float) -> list[dict]:
        """Find available contract farming opportunities matching farmer profile."""
        estimated_yield = 2.5  # tonnes/ha (conservative)
        total_tonnes = estimated_yield * farm_size_ha

        matches = []
        for offer in self.CONTRACT_FARMING_OFFERS:
            if offer["crop"] == crop and total_tonnes >= offer["min_tonnes"]:
                match_score = min(100, total_tonnes / offer["min_tonnes"] * 50)
                matches.append({
                    **offer,
                    "estimated_total_value_kes": round(offer["price_kes_per_tonne"] * total_tonnes),
                    "match_score": round(match_score),
                    "your_estimated_tonnes": round(total_tonnes, 1),
                })

        matches.sort(key=lambda m: m["match_score"], reverse=True)
        return matches

    async def get_idle_land_opportunity(self, latitude: float, longitude: float, farm_size_ha: float) -> dict:
        """Calculate the investment return of bringing idle land into production."""
        from .land_intelligence import LandIntelligence

        land = LandIntelligence(self.power)
        idle = await land.detect_idle_land_risk(latitude, longitude)
        suit = await land.analyse_land_suitability(latitude, longitude, "", farm_size_ha)

        if idle["idle_risk"] == "active":
            return {"message": "Land is already in use.", "idle_risk": "active"}

        best = suit["crop_recommendations"][0] if suit["crop_recommendations"] else None
        if not best:
            return {"error": "Could not determine best crop"}

        yield_data = await land.estimate_yield(latitude, longitude, best["crop"], farm_size_ha)
        price = await self.get_best_price(best["crop"].lower().replace(" ", "_"), yield_data["total_yield_tonnes"])

        development_cost_kes = farm_size_ha * 50000  # KES 50k/ha for clearing, planting, first irrigation

        return {
            "idle_risk": idle["idle_risk"],
            "farm_size_ha": farm_size_ha,
            "best_crop": best["crop"],
            "suitability_score": best["suitability_score"],
            "estimated_yield_tonnes": yield_data["total_yield_tonnes"],
            "estimated_gross_revenue_kes": yield_data["gross_revenue_kes"],
            "development_cost_kes": round(development_cost_kes),
            "net_first_year_return_kes": round(yield_data["gross_revenue_kes"] - development_cost_kes),
            "roi_first_year_pct": round((yield_data["gross_revenue_kes"] - development_cost_kes) / development_cost_kes * 100, 1),
            "contract_farming_available": len(await self.find_contract_farming("", best["crop"], farm_size_ha)) > 0,
        }

    async def get_best_feed_price(self, dairy_cows: int = 1) -> dict:
        """Find the best animal feed prices and options."""
        daily_feed_kg_per_cow = 12  # Typical dairy cow
        total_daily_kg = daily_feed_kg_per_cow * dairy_cows
        total_monthly_kg = total_daily_kg * 30

        results = []
        for supplier in self.ANIMAL_FEED_SUPPLIERS:
            monthly_cost = total_monthly_kg * supplier["dairy_meal_kes_kg"]
            results.append({
                "supplier": supplier["name"],
                "location": supplier["location"],
                "price_per_kg_kes": supplier["dairy_meal_kes_kg"],
                "quality_score": supplier["quality_score"],
                "monthly_cost_kes": round(monthly_cost),
                "annual_cost_kes": round(monthly_cost * 12),
                "value_score": round(supplier["quality_score"] / supplier["dairy_meal_kes_kg"] * 100, 1),
            })

        results.sort(key=lambda r: r["value_score"], reverse=True)
        return {
            "dairy_cows": dairy_cows,
            "daily_feed_kg": total_daily_kg,
            "monthly_feed_kg": round(total_monthly_kg),
            "suppliers": results,
            "best_value": results[0],
            "potential_annual_savings_kes": round((max(r["monthly_cost_kes"] for r in results) - min(r["monthly_cost_kes"] for r in results)) * 12),
        }
