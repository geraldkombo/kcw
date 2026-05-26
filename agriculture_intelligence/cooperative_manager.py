"""Cooperative manager — solves mismanagement of cooperatives (milk pricing, animal feeds,
governance tracking, collective bargaining optimisation)."""

from typing import Any


class CooperativeManager:
    """Manages cooperative operations: milk pricing, feed procurement, governance,
    collective bargaining, and member value optimisation."""

    # Reference data on cooperatives
    COOPERATIVE_BENCHMARKS = {
        "milk_price_per_litre": {"well_managed": 55, "average": 45, "poorly_managed": 35, "market_rate": 52},
        "feed_cost_per_kg": {"well_managed": 36, "average": 40, "poorly_managed": 46, "market_rate": 42},
        "member_satisfaction_pct": {"well_managed": 85, "average": 60, "poorly_managed": 35},
        "default_rate_pct": {"well_managed": 3, "average": 8, "poorly_managed": 18},
    }

    def __init__(self):
        pass

    async def assess_cooperative_health(
        self, member_count: int, avg_milk_price_kes: float,
        avg_feed_cost_kes: float, default_rate_pct: float,
    ) -> dict:
        """Score a cooperative's financial health and member value."""
        benchmarks = self.COOPERATIVE_BENCHMARKS

        # Price score
        price_score = min(100, avg_milk_price_kes / benchmarks["milk_price_per_litre"]["market_rate"] * 100)
        feed_score = max(0, 100 - (avg_feed_cost_kes / benchmarks["feed_cost_per_kg"]["market_rate"] * 100 - 100))
        default_score = max(0, 100 - default_rate_pct * 5)

        overall = round((price_score * 0.4 + feed_score * 0.3 + default_score * 0.3), 1)

        leakage = (benchmarks["milk_price_per_litre"]["well_managed"] - avg_milk_price_kes) * member_count * 5 * 365  # 5L/cow/day avg

        return {
            "member_count": member_count,
            "avg_milk_price_kes": avg_milk_price_kes,
            "avg_feed_cost_kes": avg_feed_cost_kes,
            "default_rate_pct": default_rate_pct,
            "health_score": overall,
            "grade": "A" if overall >= 80 else "B" if overall >= 65 else "C" if overall >= 45 else "D",
            "price_score": round(price_score, 1),
            "feed_score": round(feed_score, 1),
            "default_score": round(default_score, 1),
            "estimated_annual_leakage_kes": round(leakage),
            "leakage_per_member_kes": round(leakage / member_count) if member_count > 0 else 0,
        }

    async def optimize_milk_pricing(self, current_price: float, volume_litres_daily: float) -> dict:
        """Optimise milk pricing strategy for maximum member value."""
        market_rate = 52
        premium_rate = 55  # Direct sale / branded
        bulk_rate = 48  # Processor bulk

        if current_price < 45:
            # Poor pricing — likely middlemen exploitation
            gap = market_rate - current_price
            additional_revenue_daily = gap * volume_litres_daily
            strategies = [
                {
                    "strategy": "Bulk chilling & direct processor contract",
                    "expected_price_kes": premium_rate,
                    "gain_kes_litre": round(premium_rate - current_price, 1),
                    "additional_daily_revenue_kes": round((premium_rate - current_price) * volume_litres_daily),
                    "investment_needed_kes": 250000,
                    "payback_days": round(250000 / ((premium_rate - current_price) * volume_litres_daily)),
                },
                {
                    "strategy": "Form milk processing (yoghurt, mala)",
                    "expected_price_kes": premium_rate + 15,
                    "gain_kes_litre": round(premium_rate + 15 - current_price, 1),
                    "additional_daily_revenue_kes": round((premium_rate + 15 - current_price) * volume_litres_daily * 0.5),
                    "investment_needed_kes": 800000,
                    "payback_days": 0,
                },
            ]
        else:
            strategies = [{"strategy": "Maintain current pricing", "expected_price_kes": current_price, "gain_kes_litre": 0}]

        return {
            "current_price_kes": current_price,
            "daily_volume_litres": volume_litres_daily,
            "market_rate_kes": market_rate,
            "annual_milk_revenue_kes": round(current_price * volume_litres_daily * 365),
            "optimization_strategies": strategies,
            "recommended_strategy": strategies[0]["strategy"] if strategies else None,
            "estimated_annual_gain_kes": round(strategies[0].get("additional_daily_revenue_kes", 0) * 365) if strategies else 0,
        }

    async def optimize_feed_procurement(self, members: int, cows_per_member: float = 2.0) -> dict:
        """Optimise collective animal feed procurement for cooperative members."""
        total_cows = members * cows_per_member
        daily_feed_kg = total_cows * 12  # 12kg/cow/day
        monthly_feed_kg = daily_feed_kg * 30
        annual_feed_kg = monthly_feed_kg * 12

        # Bulk purchasing power
        bulk_discount = min(25, members * 0.5)
        if bulk_discount < 5:
            bulk_discount = 0

        individual_price = 42  # KES/kg retail
        bulk_price = individual_price * (1 - bulk_discount / 100)

        savings_daily = (individual_price - bulk_price) * daily_feed_kg
        savings_monthly = savings_daily * 30
        savings_annual = savings_daily * 365

        return {
            "members": members,
            "total_cows": round(total_cows),
            "daily_feed_kg": round(daily_feed_kg),
            "monthly_feed_kg": round(monthly_feed_kg),
            "annual_feed_kg": round(annual_feed_kg),
            "individual_price_kes_kg": individual_price,
            "bulk_price_kes_kg": round(bulk_price, 1),
            "bulk_discount_pct": round(bulk_discount, 1),
            "daily_savings_kes": round(savings_daily),
            "monthly_savings_kes": round(savings_monthly),
            "annual_savings_kes": round(savings_annual),
            "savings_per_member_annual_kes": round(savings_annual / members),
            "recommendation": (
                f"With {members} members, collective feed procurement saves KES {savings_annual:,.0f}/year "
                f"(KES {savings_annual/members:,.0f}/member). Register as a cooperative buying group."
            ),
        }

    async def get_governance_recommendations(self, health_score: float, member_count: int) -> list[dict]:
        """Generate governance improvement recommendations based on cooperative health."""
        recs = []

        if health_score < 50:
            recs.append({
                "area": "Governance structure",
                "issue": "Cooperative appears distressed",
                "recommendation": "Elect new management committee with quarterly AGMs. Install transparent digital record-keeping.",
                "impact": "Can improve member trust and reduce leakage by 30-50%",
                "cost_kes": 100000,
            })
        if health_score < 65:
            recs.append({
                "area": "Price transparency",
                "issue": "Milk prices below market rate",
                "recommendation": "Implement daily SMS price notifications to all members. Negotiate directly with processors.",
                "impact": "Expected KES 5-10/litre price improvement",
                "cost_kes": 50000,
            })
        recs.append({
            "area": "Bulk procurement",
            "issue": f"Individual feed purchasing by {member_count} members",
            "recommendation": f"Centralise feed procurement for {member_count} members to access bulk discounts of 10-25%.",
            "impact": f"Saves KES {member_count * 2 * 12 * 365 * 6:,}/year at current prices",
            "cost_kes": 20000,
        })
        recs.append({
            "area": "Digital ledger",
            "issue": "Manual record-keeping leads to leakage and disputes",
            "recommendation": "Deploy blockchain-based cooperative ledger for transparent milk collection, pricing, and payouts.",
            "impact": "Eliminates 'missing litres', builds member trust, auditable by KCC/KRA",
            "cost_kes": 150000,
        })

        return recs
