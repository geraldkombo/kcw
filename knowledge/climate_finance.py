from __future__ import annotations

"""Climate finance and de-risking intelligence for Kenya's traditional food systems.

Synthesizes data on parametric insurance, sovereign green bonds, bilateral aid contraction,
post-harvest loss economics, and carbon credit potential into a unified de-risking framework.

Sources:
  - Kenya National Assembly Budget Committee hearing on climate adaptation financing (May 2026)
  - USAID Executive Order 14169 impact assessment (2025-2026)
  - Ojwang, H.J. (2020) — women farmers' indigenous knowledge, Homa Bay County
  - Traditional food knowledge — Kenya AI Challenge workshop (2026)
"""


class ClimateFinanceKnowledge:
    """De-risking knowledge layer — parametric insurance, green finance, macro context.

    Ties satellite-driven precision farming data to real-world climate adaptation
    financing decisions. Every method provides structured data for the API and agents.
    """

    PARAMETRIC_INSURANCE_MODEL = {
        "description": (
            "Satellite-triggered index insurance that pays out automatically when "
            "remote-sensed weather data crosses predefined thresholds — no human "
            "adjuster needed. Cuts cost by eliminating field assessment."
        ),
        "trigger_metrics": [
            {
                "name": "rainfall_deficit",
                "sensor": "NASA POWER / CHIRPS",
                "threshold": "< 60% of 10-year mean over 30 consecutive days",
                "payout_formula": "KES 5,000 per mm below threshold per hectare",
                "max_tenure": 10,
            },
            {
                "name": "land_surface_temperature",
                "sensor": "NASA POWER / MODIS",
                "threshold": "> 38°C for 7 consecutive days during growing season",
                "payout_formula": "KES 3,000 per day exceeding threshold per hectare",
                "max_tenure": 14,
            },
            {
                "name": "vegetation_index_anomaly",
                "sensor": "NASA POWER / VIIRS",
                "threshold": "NDVI < 0.3 during peak growing season",
                "payout_formula": "KES 4,000 per 0.1 below threshold per hectare",
                "max_tenure": 10,
            },
        ],
        "regulatory_context": {
            "kenya_2026_proposal": "Insurers must settle weather-related parametric claims within 10 days",
            "regulator": "Insurance Regulatory Authority of Kenya (IRA)",
            "status": "proposed regulation, 2026",
        },
        "target_crops": [
            "amaranth", "cowpea_leaves", "sorghum", "finger_millet",
            "pigeon_pea", "bambara_nut", "dek", "mito", "boo", "ndemra",
        ],
        "farmer_benefit": (
            "Rapid liquidity allows replanting fast-maturing indigenous crops "
            "(21-45 day cycle) within the same rainy season — prevents total "
            "crop failure from cascading into household famine."
        ),
        "premium_estimate_kes_per_ha": "3,000–8,000 (subsidised via green bond premium support)",
    }

    GREEN_BOND_FRAMEWORK = {
        "description": (
            "Kenya's $772M (KES 100B) sovereign green bond targeting climate-smart "
            "farming. Proceeds ring-fenced for agricultural environmental adaptation. "
            "5-10 year maturity targeting institutional investors, pension funds, diaspora."
        ),
        "allocations": [
            {
                "program": "Solar-powered cold storage infrastructure",
                "allocation_pct": 35,
                "target": "Village-level cold rooms at aggregation centres",
                "impact": "Cut 57% post-harvest loss rate of indigenous vegetables",
            },
            {
                "program": "Climate-resilient seed systems",
                "allocation_pct": 25,
                "target": "Indigenous seed multiplication and distribution in ASALs",
                "impact": "Deploy drought-tolerant traditional varieties to 500K farmers",
            },
            {
                "program": "Parametric insurance premium support",
                "allocation_pct": 20,
                "target": "Subsidise premiums for 1M smallholder farmers",
                "impact": "Scale satellite-triggered index insurance to poorest farmers",
            },
            {
                "program": "Regenerative farming & carbon credit infrastructure",
                "allocation_pct": 20,
                "target": "MRV systems, training, certification for carbon credits",
                "impact": "Transform intercropping carbon sequestration into revenue stream",
            },
        ],
        "instruments": ["5-year green bond", "7-year green bond", "10-year green bond"],
        "target_investors": ["Institutional investors", "International pension funds", "Kenyan diaspora"],
    }

    USAID_FREEZE_IMPACT = {
        "description": (
            "Executive Order 14169 (Jan 2025) initiated systemic freeze on USAID funding. "
            "Kenya historically received ~$470M/year from USAID (~80% to public health). "
            "Agricultural extension, KIAMIS data system, and CSA training programs suspended."
        ),
        "key_metrics": {
            "bilateral_aid_contraction_usd": "$225M",
            "award_termination_rate_pct": "70–86",
            "agricultural_extension_status": "halted — unfunded county governments",
            "csa_mainstreamed_in_counties_pct": 87,
            "csa_budget_allocated_pct": 42,
            "health_infrastructure_impact": "Mass termination of field staff and contractors",
            "food_insecurity_estimate_2026": "19M people (WFP)",
        },
        "systemic_consequence": (
            "The withdrawal of donor-funded extension services has shifted the burden "
            "entirely onto underfunded county governments. Indigenous crops requiring "
            "zero external inputs — commercial seed, chemical fertiliser, irrigation — "
            "have shifted from cultural preference to absolute economic survival."
        ),
    }

    POST_HARVEST_LOSS_DATA = {
        "aiv_phl_rate_pct": 57,
        "economic_burden_ratio_farmer_vs_retailer": 7.6,
        "primary_causes": [
            "Absence of refrigerated transport at rural aggregation nodes",
            "Rapid turgidity loss in indigenous vegetables (24-48h shelf life)",
            "Multiple handling points in fragmented value chain",
            "Lack of cold storage at farm level",
        ],
        "interventions": [
            {
                "solution": "Solar-powered cold rooms at village aggregation centres",
                "phl_reduction_pct": 45,
                "cost_per_unit_kes": "KES 150K–300K per 5-tonne unit",
                "funding_source": "Green bond allocation (35%)",
            },
            {
                "solution": "Pre-cooked vacuum-packed AIVs",
                "phl_reduction_pct": 70,
                "cost_per_unit_kes": "KES 50K processing line per group",
                "funding_source": "Chama group investment / SACCO loan",
                "premium_retail_price_kes": "400 KES/pack (vs 55 KES/kg fresh)",
            },
        ],
    }

    DOMESTIC_FISCAL_CONTEXT = {
        "disaster_response_budget_kes": "75 million KES (across all departments, 2026 supplementary)",
        "national_budget_context": (
            "Kenya's 2026 supplementary budget allocates a microscopic fraction of actual "
            "macroeconomic damages from consecutive droughts and floods to disaster response. "
            "A $2 billion Eurobond repayment (2024) severely constrains discretionary spending."
        ),
        "debt_burden_context": "$2 billion Eurobond repayment (2024) constrains fiscal space for climate adaptation",
        "fiscal_stance": "reactive rather than proactive regarding climate shocks",
    }

    PUBLIC_HEALTH_NUTRITION = {
        "stunting_rate_2008_pct": 35,
        "stunting_rate_2014_pct": 26,
        "stunting_trend": "declining but entrenched — 2026 climate/fiscal shocks exacerbate fragility",
        "hidden_hunger_context": (
            "Systemic transition from indigenous diets to refined exotic staples has created "
            "a dual burden: caloric inadequacy + acute micronutrient deficiencies. Rural families "
            "subsist on energy-dense nutrient-poor staples (ugali) while neglecting local nutrient-rich flora."
        ),
        "food_remittance_nairobi_hh_pct": 50,
        "food_remittance_context": "Over 50% of Nairobi households receive food remittances directly from rural relatives — a critical unmeasured buffer against urban food poverty.",
    }

    CROSS_BORDER_TRADE = {
        "women_traders_share_pct": 77,
        "women_traders_context": "Women Small-Scale Cross-Border Traders (WICBTs) dominate traditional food corridors",
        "regime": "Simplified Trade Regime (STR) — allows tariff-free movement of locally grown produce under monetary threshold",
        "barriers": [
            "Non-tariff barriers at formal One Stop Border Posts (OSBPs)",
            "Rampant extortion by border officials",
            "Arbitrary municipal taxation",
            "Severe bureaucratic bottlenecks",
        ],
        "informal_crossing": (
            "Panya routes — informal ungazetted crossing points used by women to avoid rapid "
            "spoilage of perishable vegetable cargo. Expedites transit but exposes women to "
            "severe harassment, physical violence, and confiscation of goods."
        ),
    }

    CARBON_CREDIT_POTENTIAL = {
        "description": (
            "Traditional intercropping systems (sorghum-cowpea, pigeonpea-maize) "
            "build soil organic carbon through continuous root mass turnover, "
            "nitrogen fixation, and reduced tillage. Quantifiable for carbon markets."
        ),
        "estimated_sequestration_tonnes_co2_per_ha": {
            "sorghum_cowpea_intercrop": 2.5,
            "agroforestry_legume_trees": 5.0,
            "traditional_polyculture_lake_region": 3.2,
            "maize_monoculture_reference": -0.5,
        },
        "carbon_price_kes_per_tonne": "2,000–4,000 (voluntary market, 2026)",
        "additional_revenue_kes_per_ha": "5,000–20,000 depending on system",
        "standards": ["Verra (VCS)", "Gold Standard", "Plan Vivo (for smallholders)"],
    }

    def get_parametrics(self, county: str | None = None) -> dict:
        return {
            "model": self.PARAMETRIC_INSURANCE_MODEL,
            "county_context": self._get_county_risk_profile(county),
        }

    def get_green_bond_summary(self) -> dict:
        return self.GREEN_BOND_FRAMEWORK

    def get_usaid_impact(self) -> dict:
        return self.USAID_FREEZE_IMPACT

    def get_phl_analysis(self, crop: str | None = None) -> dict:
        return self.POST_HARVEST_LOSS_DATA

    def get_carbon_potential(self, system: str | None = None) -> dict:
        return self.CARBON_CREDIT_POTENTIAL

    def get_de_risk_overview(self) -> dict:
        return {
            "thesis": (
                "The convergence of four forces makes traditional food systems "
                "the only viable path forward for Kenya's food security in 2026:"
            ),
            "forces": [
                {
                    "name": "Climate crisis",
                    "detail": (
                        "IPCC projects +2–4°C and 20% rainfall reduction by 2050. "
                        "Exotic crops (maize, kale) fail catastrophically under these conditions. "
                        "Indigenous crops (Rs 0.78–1.00) thrive with minimal inputs."
                    ),
                    "data_sources": ["NASA POWER", "Open-Meteo ERA5", "CROP_INDEX resilience scores"],
                },
                {
                    "name": "Funding collapse",
                    "detail": (
                        "Executive Order 14169 froze ~$470M/year USAID funding. "
                        "86% of awards terminated. Agricultural extension halted. "
                        "Zero-funded CSA programs. Indigenous crops need no external inputs."
                    ),
                    "data_sources": ["USAID_FREEZE_IMPACT"],
                },
                {
                    "name": "Innovation maturity",
                    "detail": (
                        "Satellite data (NASA POWER, MODIS, VIIRS) enables parametric insurance "
                        "with 10-day payouts. Green bond provides $772M for cold chains and seeds. "
                        "Mobile money enables last-mile premium collection and claims disbursement."
                    ),
                    "data_sources": ["PARAMETRIC_INSURANCE_MODEL", "GREEN_BOND_FRAMEWORK"],
                },
                {
                    "name": "Knowledge validation",
                    "detail": (
                        "Ojwang (2020) and the wider traditional food knowledge base "
                        "document ~50+ indigenous crops, seed-bank practices, intercropping "
                        "matrices, and women-led market corridors. This is not anecdote — "
                        "it is structured, quantified, data-ready knowledge."
                    ),
                    "data_sources": ["TraditionalFoodsIndex", "NUTRITION_MINERALS", "INTERCROPPING_PATTERNS"],
                },
            ],
            "verdict": (
                "Idea whose time has come. The pieces exist: satellite data, "
                "parametric insurance, green finance, validated indigenous knowledge, "
                "mobile money rails, and a population that never stopped growing and "
                "eating these crops. What was missing — a unified data layer that "
                "makes the invisible visible and the informal investable — is what "
                "Food Roots KE provides."
            ),
        }

    def _get_county_risk_profile(self, county: str | None) -> dict:
        profiles = {
            "homa bay": {
                "primary_risk": "Flooding (Lake Victoria basin) + drought",
                "recommended_crops": ["dek", "mito", "boo", "black_nightshade", "cassava"],
                "parametric_suitability": "high — lake zone has reliable satellite coverage",
            },
            "kitui": {
                "primary_risk": "Drought (ASAL)",
                "recommended_crops": ["cowpea_leaves", "pigeon_pea", "sorghum", "baobab", "tamarind"],
                "parametric_suitability": "very_high — clear rainfall deficit triggers",
            },
            "turkana": {
                "primary_risk": "Extreme drought + heat",
                "recommended_crops": ["desert_date", "bird_plum", "sorghum"],
                "parametric_suitability": "high — temperature and NDVI triggers most effective",
            },
        }
        if county and county.lower() in profiles:
            return profiles[county.lower()]
        return {"note": "Generic risk profile — use satellite data for precise assessment"}
