"""Investment advisor — AI-driven agricultural investment recommendations.
Analyses land, water, solar, seed, market, and cooperative data to recommend
the highest-return agricultural investments. This is the system that makes
AI-driven agriculture investments, not just another app."""

from satellite.power_client import PowerClient
from .land_intelligence import LandIntelligence
from .water_optimizer import WaterOptimizer
from .solar_optimizer import SolarOptimizer
from .seed_quality import SeedQualityAnalyzer
from .market_intelligence import MarketIntelligence
from .cooperative_manager import CooperativeManager
from .precision_farming import PrecisionFarming


class InvestmentAdvisor:
    """Autonomous agricultural investment advisor. Combines all intelligence
    modules to recommend optimal agricultural investments with quantified returns."""

    INVESTMENT_TYPES = {
        "land_development": {
            "name": "Idle Land Development",
            "min_kes": 100000,
            "max_kes": 5000000,
            "typical_roi_pct": 35,
            "risk": "medium",
            "description": "Bring idle farmland into production with irrigation, seed, and soil prep.",
        },
        "irrigation_infrastructure": {
            "name": "Solar Irrigation System",
            "min_kes": 80000,
            "max_kes": 500000,
            "typical_roi_pct": 45,
            "risk": "low",
            "description": "Solar-powered drip irrigation — leverages equatorial sun to derisk water.",
        },
        "seed_optimization": {
            "name": "Premium Seed Investment",
            "min_kes": 10000,
            "max_kes": 100000,
            "typical_roi_pct": 60,
            "risk": "low",
            "description": "Upgrade to certified drought-resistant seed varieties with proven germination.",
        },
        "cooperative_modernization": {
            "name": "Cooperative Digital Transformation",
            "min_kes": 50000,
            "max_kes": 500000,
            "typical_roi_pct": 80,
            "risk": "medium",
            "description": "Digital ledgers, bulk procurement, direct processor contracts for cooperatives.",
        },
        "contract_farming": {
            "name": "Contract Farming Scale-Up",
            "min_kes": 200000,
            "max_kes": 2000000,
            "typical_roi_pct": 25,
            "risk": "low",
            "description": "Expand production under guaranteed off-take agreement with processor.",
        },
        "solar_drying": {
            "name": "Solar Drying Infrastructure",
            "min_kes": 50000,
            "max_kes": 300000,
            "typical_roi_pct": 40,
            "risk": "low",
            "description": "Post-harvest solar driers reduce losses 30-50%, improve crop quality and price.",
        },
    }

    def __init__(
        self,
        power: PowerClient | None = None,
        land: LandIntelligence | None = None,
        water: WaterOptimizer | None = None,
        solar: SolarOptimizer | None = None,
        seed: SeedQualityAnalyzer | None = None,
        market: MarketIntelligence | None = None,
        cooperative: CooperativeManager | None = None,
        precision: PrecisionFarming | None = None,
    ):
        self.power = power or PowerClient()
        self.land = land or LandIntelligence(self.power)
        self.water = water or WaterOptimizer(self.power)
        self.solar = solar or SolarOptimizer(self.power)
        self.seed = seed or SeedQualityAnalyzer(self.power)
        self.market = market or MarketIntelligence(self.power)
        self.coop = cooperative or CooperativeManager()
        self.pf = precision or PrecisionFarming(self.power)

    async def recommend_investments(
        self,
        latitude: float,
        longitude: float,
        county: str,
        farm_size_ha: float = 1.0,
        budget_kes: float = 500000,
        crop: str = "maize",
        cooperative_members: int = 0,
        dairy_cows: int = 0,
    ) -> dict:
        """Generate ranked agricultural investment recommendations."""
        # Gather all intelligence
        land_suitability = await self.land.analyse_land_suitability(latitude, longitude, county, farm_size_ha)
        idle_risk = await self.land.detect_idle_land_risk(latitude, longitude)
        yield_projection = await self.land.estimate_yield(latitude, longitude, crop, farm_size_ha)
        water_deficit = await self.water.compute_water_deficit(latitude, longitude, crop, farm_size_ha=farm_size_ha)
        solar_advantage = await self.solar.get_solar_advantage(latitude, longitude)
        seed_recommendation = await self.seed.recommend_best_seed(crop, latitude, longitude)
        market_price = await self.market.get_best_price(crop, yield_projection.get("total_yield_tonnes", 1))
        idle_opportunity = await self.market.get_idle_land_opportunity(latitude, longitude, farm_size_ha)
        feed_optimization = None
        coop_health = None
        if dairy_cows > 0:
            feed_optimization = await self.market.get_best_feed_price(dairy_cows)
        if cooperative_members > 0:
            coop_health = await self.coop.assess_cooperative_health(cooperative_members, 45, 42, 8)

        # Precision farming intelligence (equatorial general agriculture)
        gdd = await self.pf.compute_gdd(latitude, longitude, crop)
        et = await self.pf.compute_et_penman_monteith(latitude, longitude)
        pest = await self.pf.assess_pest_disease_risk(latitude, longitude, crop)
        micro = await self.pf.classify_micro_climate(latitude, longitude)
        frost = await self.pf.assess_frost_risk(latitude, longitude)
        timing = await self.pf.get_precision_irrigation_timing(latitude, longitude)
        vrate = await self.pf.get_variable_rate_recommendation(latitude, longitude, farm_size_ha)

        # Precision farming adjustments
        pest_multiplier = 1.0
        if pest.get("overall_risk") == "high":
            pest_multiplier = 1.3  # Pest pressure increases value of seed upgrade + IPM
        if frost.get("frost_risk") in ("severe", "high"):
            frost_multiplier = 0.7  # Frost risk reduces expected returns
        else:
            frost_multiplier = 1.0

        # Generate investment opportunities
        opportunities = []
        precision_context = {
            "gdd_per_day": gdd.get("gdd_per_day"),
            "days_to_harvest": gdd.get("estimated_days_to_harvest"),
            "et0_mm_day": et.get("et0_mm_day"),
            "pest_risks": [r["pest"] for r in pest.get("active_risks", [])],
            "micro_climate_zone": micro.get("zone"),
            "frost_risk": frost.get("frost_risk"),
            "irrigation_timing": timing.get("optimal_irrigation_time"),
            "variable_rate_saving_pct": vrate.get("water_saving_vs_uniform_pct"),
        }

        # 1. Seed optimization (always relevant)
        seed_cost = seed_recommendation.get("all_options", [{}])[0].get("cost_kes_per_ha", 10000) if seed_recommendation.get("all_options") else 10000
        seed_revenue = seed_recommendation.get("all_options", [{}])[0].get("estimated_revenue_kes_ha", 50000) if seed_recommendation.get("all_options") else 50000
        if budget_kes >= seed_cost:
            seed_roi = (seed_revenue - seed_cost) / seed_cost * 100 * pest_multiplier * frost_multiplier
            opp = {
                "type": "seed_optimization",
                "name": f"Upgrade to {seed_recommendation.get('recommended_variety', 'premium')} seed",
                "investment_kes": round(seed_cost * farm_size_ha),
                "expected_return_kes": round((seed_revenue - seed_cost) * farm_size_ha * pest_multiplier * frost_multiplier),
                "roi_pct": round(seed_roi, 1),
                "risk": "low",
                "timeframe_months": 4,
                "detail": f"Switch from local varieties to {seed_recommendation.get('recommended_variety')} — "
                          f"{seed_recommendation.get('reason', '')}",
            }
            if pest.get("overall_risk") == "high":
                opp["detail"] += f" Pest pressure high ({pest['total_risk_count']} risks) — disease-resistant seed provides additional protection."
            if frost.get("frost_risk") in ("severe", "high"):
                opp["detail"] += f" Frost risk ({frost['frost_risk']}) — consider frost-tolerant varieties."
            opportunities.append(opp)

        # 2. Irrigation if water deficit exists
        if water_deficit.get("daily_irrigation_need_mm", 0) > 0.5:
            irrigation_cost = int(80000 * farm_size_ha)  # Solar drip system
            water_savings = int(water_deficit.get("annual_irrigation_cost_kes", 50000) * 0.6)
            if budget_kes >= irrigation_cost:
                opportunities.append({
                    "type": "irrigation_infrastructure",
                    "name": "Solar-powered drip irrigation",
                    "investment_kes": irrigation_cost,
                    "expected_return_kes": water_savings + int(yield_projection.get("gross_revenue_kes", 50000) * 0.4),
                    "roi_pct": round((water_savings + yield_projection.get("gross_revenue_kes", 50000) * 0.4) / irrigation_cost * 100, 1),
                    "risk": "low",
                    "timeframe_months": 18,
                    "detail": water_deficit.get("recommendation", ""),
                })

        # 3. Idle land development
        if idle_risk.get("idle_risk") in ("idle", "underutilised") and isinstance(idle_opportunity, dict) and idle_opportunity.get("roi_first_year_pct", 0) > 0:
            dev_cost = int(idle_opportunity.get("development_cost_kes", 50000))
            if budget_kes >= dev_cost:
                opportunities.append({
                    "type": "land_development",
                    "name": f"Develop {farm_size_ha}ha idle land for {idle_opportunity.get('best_crop', crop)}",
                    "investment_kes": dev_cost,
                    "expected_return_kes": idle_opportunity.get("net_first_year_return_kes", 0),
                    "roi_pct": idle_opportunity.get("roi_first_year_pct", 0),
                    "risk": "medium",
                    "timeframe_months": 6,
                    "detail": f"Idle land detected. Best crop: {idle_opportunity.get('best_crop')} "
                              f"(score: {idle_opportunity.get('suitability_score')}). "
                              f"Contract farming: {'available' if idle_opportunity.get('contract_farming_available') else 'check spot market'}.",
                })

        # 4. Solar drying
        solar_drying_cost = int(50000 * farm_size_ha)
        if solar_advantage.get("solar_drying_potential") in ("excellent", "good") and budget_kes >= solar_drying_cost:
            opportunities.append({
                "type": "solar_drying",
                "name": "Solar drying infrastructure",
                "investment_kes": solar_drying_cost,
                "expected_return_kes": int(yield_projection.get("gross_revenue_kes", 50000) * 0.2),
                "roi_pct": round(yield_projection.get("gross_revenue_kes", 50000) * 0.2 / solar_drying_cost * 100, 1),
                "risk": "low",
                "timeframe_months": 3,
                "detail": f"Equatorial solar ({solar_advantage.get('current_solar_kwh_m2_day')} kWh/m2/day) "
                          f"enables efficient solar drying. Reduces post-harvest losses 30-50%.",
            })

        # 5. Contract farming (opportunity, not capital cost — just certification + quality)
        if market_price.get("best_contract_farming"):
            cf = market_price["best_contract_farming"]
            cf_cert_cost = int(25000 * farm_size_ha)  # Certification + quality control cost
            total_yield_tonnes = yield_projection.get("total_yield_tonnes", 1)
            spot_revenue = market_price.get("current_price_kes_tonne", 0) * total_yield_tonnes
            contract_revenue = cf.get("price_kes_per_tonne", 0) * total_yield_tonnes
            premium_revenue = contract_revenue - spot_revenue
            net_return = premium_revenue - cf_cert_cost
            if net_return > 0 and budget_kes >= cf_cert_cost:
                opportunities.append({
                    "type": "contract_farming",
                    "name": f"Contract farming: {cf.get('buyer')}",
                    "investment_kes": cf_cert_cost,
                    "expected_return_kes": round(net_return),
                    "roi_pct": round(net_return / cf_cert_cost * 100, 1),
                    "risk": "low",
                    "timeframe_months": cf.get("duration_months", 12),
                    "detail": f"{cf.get('buyer')} offers KES {cf.get('price_kes_per_tonne'):,}/tonne "
                              f"(KES {(cf.get('price_kes_per_tonne',0) - market_price.get('current_price_kes_tonne',0)):,}/tonne above spot). "
                              f"Certification cost KES {cf_cert_cost:,}. Min {cf.get('min_tonnes')} tonnes.",
                })

        # 6. Cooperative modernization
        if cooperative_members >= 5:
            coop_cost = 150000
            if budget_kes >= coop_cost:
                coop_savings = 50000 * cooperative_members  # Estimated savings from bulk procurement
                opportunities.append({
                    "type": "cooperative_modernization",
                    "name": f"Digital transformation for {cooperative_members}-member cooperative",
                    "investment_kes": coop_cost,
                    "expected_return_kes": coop_savings,
                    "roi_pct": round(coop_savings / coop_cost * 100, 1),
                    "risk": "medium",
                    "timeframe_months": 6,
                    "detail": f"Digital ledger + bulk procurement + direct processor contracts. "
                              f"Estimated KES {coop_savings:,.0f}/year savings across {cooperative_members} members.",
                })

        # 7. Feed optimization
        if dairy_cows > 0 and feed_optimization:
            annual_savings = feed_optimization.get("potential_annual_savings_kes", 0)
            if annual_savings > 10000:
                opportunities.append({
                    "type": "feed_optimization",
                    "name": f"Optimize feed for {dairy_cows} dairy cows",
                    "investment_kes": 20000,
                    "expected_return_kes": annual_savings,
                    "roi_pct": round(annual_savings / 20000 * 100, 1),
                    "risk": "low",
                    "timeframe_months": 1,
                    "detail": f"Switch from {feed_optimization.get('suppliers', [{}])[0].get('supplier', 'current')} "
                              f"to best-value supplier. Save ~KES {annual_savings:,.0f}/year.",
                })

        # Rank by ROI
        opportunities.sort(key=lambda o: o["roi_pct"], reverse=True)

        # Budget filter
        affordable = [o for o in opportunities if o["investment_kes"] <= budget_kes]
        total_investment = sum(o["investment_kes"] for o in affordable)
        total_return = sum(o["expected_return_kes"] for o in affordable)

        return {
            "location": {"county": county, "latitude": latitude, "longitude": longitude},
            "farm_size_ha": farm_size_ha,
            "budget_kes": budget_kes,
            "recommended_crop": land_suitability.get("best_crop"),
            "equatorial_solar_advantage_pct": solar_advantage.get("equatorial_advantage_pct"),
            "current_water_deficit_mm_day": water_deficit.get("daily_irrigation_need_mm", 0),
            "idle_land_status": idle_risk.get("idle_risk"),
            "soil_health": land_suitability.get("soil_health", {}).get("description"),
            "precision_farming": precision_context,
            "ranked_opportunities": affordable,
            "total_investment_kes": round(total_investment),
            "total_expected_return_kes": round(total_return),
            "portfolio_roi_pct": round(total_return / total_investment * 100, 1) if total_investment > 0 else 0,
            "best_first_investment": affordable[0] if affordable else None,
            "summary": (
                f"For {farm_size_ha}ha in {county} (KES {budget_kes:,.0f} budget): "
                f"{len(affordable)} viable investments totaling KES {total_investment:,.0f} "
                f"with estimated {total_return:,.0f} return ({round(total_return/total_investment*100, 1) if total_investment > 0 else 0}% ROI). "
                f"Best first step: {affordable[0]['name']} (KES {affordable[0]['investment_kes']:,}, "
                f"{affordable[0]['roi_pct']}% ROI)."
                if affordable else
                f"Budget KES {budget_kes:,.0f} too low for current opportunities. "
                f"Minimum viable investment: KES {min(o['investment_kes'] for o in opportunities):,}."
                if opportunities else
                f"No investment opportunities identified for {county}."
            ),
        }

    async def get_portfolio_diversification(self, latitude: float, longitude: float, total_budget_kes: float) -> dict:
        """Suggest optimal portfolio allocation across investment types for diversification."""
        recs = await self.recommend_investments(latitude, longitude, "", 2.0, total_budget_kes)
        opportunities = recs.get("ranked_opportunities", [])

        if not opportunities:
            return {"error": "No opportunities available"}

        # Allocate budget across top opportunities (risk-balanced)
        total_inv = sum(o["investment_kes"] for o in opportunities)
        scaling = min(1.0, total_budget_kes / total_inv) if total_inv > 0 else 0

        portfolio = []
        allocated = 0
        for opp in opportunities:
            invest = min(opp["investment_kes"] * scaling, total_budget_kes - allocated)
            if invest <= 0:
                break
            portfolio.append({**opp, "allocated_kes": round(invest)})
            allocated += invest

        return {
            "total_budget_kes": total_budget_kes,
            "total_allocated_kes": round(allocated),
            "remaining_kes": round(total_budget_kes - allocated),
            "portfolio": portfolio,
            "expected_total_return_kes": round(sum(o["allocated_kes"] * o["roi_pct"] / 100 for o in portfolio)),
            "weighted_avg_roi_pct": round(sum(o["roi_pct"] * o["allocated_kes"] for o in portfolio) / allocated, 1) if allocated > 0 else 0,
            "diversification_score": min(100, len(portfolio) * 20),
            "risk_profile": self._assess_portfolio_risk(portfolio),
        }

    def _assess_portfolio_risk(self, portfolio: list) -> str:
        risk_counts = {"low": 0, "medium": 0, "high": 0}
        for o in portfolio:
            risk_counts.get(o.get("risk", "medium"), 0)
            risk_counts[o.get("risk", "medium")] = risk_counts.get(o.get("risk", "medium"), 0) + 1
        total = sum(risk_counts.values()) or 1
        low_pct = risk_counts.get("low", 0) / total
        if low_pct >= 0.6:
            return "conservative"
        elif low_pct >= 0.3:
            return "balanced"
        return "growth"
