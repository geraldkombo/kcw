"""Agricultural intelligence API routes — land, water, solar, seed, market,
cooperative, and investment analysis endpoints."""

from fastapi import APIRouter, Depends, Query
from agents.land_intelligence_agent import LandIntelligenceAgent
from agents.market_intelligence_agent import MarketIntelligenceAgent
from agents.cooperative_agent import CooperativeAgent
from agents.investment_advisor_agent import InvestmentAdvisorAgent
from agents.precision_farming_agent import PrecisionFarmingAgent
from satellite.power_client import PowerClient

router = APIRouter(prefix="/api/v1/agri", tags=["agricultural-intelligence"])


def get_power() -> PowerClient:
    return PowerClient()


@router.post("/land-suitability")
async def analyse_land_suitability(body: dict):
    agent = LandIntelligenceAgent()
    return await agent.analyse(body)


@router.post("/market-intelligence")
async def get_market_intelligence(body: dict):
    agent = MarketIntelligenceAgent()
    return await agent.analyse(body)


@router.post("/cooperative/assess")
async def assess_cooperative(body: dict):
    agent = CooperativeAgent()
    return await agent.assess(body)


@router.post("/invest")
async def get_investment_recommendations(body: dict):
    agent = InvestmentAdvisorAgent()
    return await agent.recommend(body)


@router.get("/solar/{lat}/{lon}")
async def get_solar_data(lat: float, lon: float):
    from agriculture_intelligence.solar_optimizer import SolarOptimizer
    opt = SolarOptimizer()
    return await opt.get_solar_advantage(lat, lon)


@router.get("/water/{lat}/{lon}")
async def get_water_data(lat: float, lon: float, crop: str = "maize", farm_size: float = 1.0):
    from agriculture_intelligence.water_optimizer import WaterOptimizer
    opt = WaterOptimizer()
    return await opt.compute_water_deficit(lat, lon, crop, "loamy", farm_size)


@router.post("/seed/recommend")
async def recommend_seed(body: dict):
    from agriculture_intelligence.seed_quality import SeedQualityAnalyzer
    analyzer = SeedQualityAnalyzer()
    crop = body.get("crop", "maize")
    lat = body.get("latitude", 0.0)
    lon = body.get("longitude", 0.0)
    budget = body.get("budget_kes", 5000)
    return await analyzer.recommend_best_seed(crop, lat, lon, budget)


@router.post("/cooperative/optimize-milk")
async def optimize_milk(body: dict):
    from agriculture_intelligence.cooperative_manager import CooperativeManager
    mgr = CooperativeManager()
    return await mgr.optimize_milk_pricing(
        body.get("current_price", 45),
        body.get("daily_volume_litres", 100),
    )


@router.post("/cooperative/optimize-feed")
async def optimize_feed(body: dict):
    from agriculture_intelligence.cooperative_manager import CooperativeManager
    mgr = CooperativeManager()
    return await mgr.optimize_feed_procurement(
        body.get("members", 10),
        body.get("cows_per_member", 2),
    )


@router.get("/prices/{crop}")
async def get_crop_prices(crop: str, quantity: float = 1.0):
    from agriculture_intelligence.market_intelligence import MarketIntelligence
    mi = MarketIntelligence()
    return await mi.get_best_price(crop, quantity)


@router.post("/contract-farming/search")
async def search_contract_farming(body: dict):
    from agriculture_intelligence.market_intelligence import MarketIntelligence
    mi = MarketIntelligence()
    return await mi.find_contract_farming(
        body.get("county", ""),
        body.get("crop", "maize"),
        body.get("farm_size_ha", 1.0),
    )


@router.post("/precision-farming")
async def get_precision_farming(body: dict):
    """Full precision farming analysis — GDD, ET, pest risk, micro-climate, frost, irrigation timing.
    General equatorial agriculture intelligence for any crop."""
    agent = PrecisionFarmingAgent()
    return await agent.analyze(
        body.get("latitude", -1.0), body.get("longitude", 36.9),
        body.get("crop", "maize"), body.get("farm_size_ha", 1.0),
    )


@router.get("/precision-farming/gdd/{lat}/{lon}/{crop}")
async def get_growing_degree_days(lat: float, lon: float, crop: str = "maize", days: int = Query(30, alias="days")):
    from agriculture_intelligence.precision_farming import PrecisionFarming
    pf = PrecisionFarming()
    return await pf.compute_gdd(lat, lon, crop, days)


@router.get("/precision-farming/et/{lat}/{lon}")
async def get_evapotranspiration(lat: float, lon: float):
    from agriculture_intelligence.precision_farming import PrecisionFarming
    pf = PrecisionFarming()
    return await pf.compute_et_penman_monteith(lat, lon)


@router.get("/precision-farming/pest-risk/{lat}/{lon}/{crop}")
async def get_pest_risk(lat: float, lon: float, crop: str = "maize"):
    pf = __import__("agriculture_intelligence.precision_farming", fromlist=["PrecisionFarming"]).PrecisionFarming()
    return await pf.assess_pest_disease_risk(lat, lon, crop)


@router.get("/precision-farming/micro-climate/{lat}/{lon}")
async def get_micro_climate(lat: float, lon: float):
    pf = __import__("agriculture_intelligence.precision_farming", fromlist=["PrecisionFarming"]).PrecisionFarming()
    return await pf.classify_micro_climate(lat, lon)


@router.get("/precision-farming/irrigation-timing/{lat}/{lon}")
async def get_irrigation_timing(lat: float, lon: float):
    pf = __import__("agriculture_intelligence.precision_farming", fromlist=["PrecisionFarming"]).PrecisionFarming()
    return await pf.get_precision_irrigation_timing(lat, lon)


@router.get("/precision-farming/equatorial-benchmark/{lat}/{lon}")
async def get_equatorial_benchmark(lat: float, lon: float):
    """Compare location against benchmark equatorial agricultural systems across major zones."""
    pf = __import__("agriculture_intelligence.precision_farming", fromlist=["PrecisionFarming"]).PrecisionFarming()
    return await pf.get_equatorial_benchmark(lat, lon)


@router.get("/precision-farming/climate-resilience/{lat}/{lon}")
async def get_climate_resilience(
    lat: float, lon: float, crop: str = "maize",
    farm_size: float = 1.0, crop_value: float = 50.0, yield_kg: float = 2000.0,
):
    """Climate adaptation ROI analysis — cost of precision farming vs. disaster response.
    References Kenya Budget Committee testimony (May 2026): 75M KES disaster response,
    zero-funded Climate Smart Agriculture programs, no crop insurance allocation."""
    pf = __import__("agriculture_intelligence.precision_farming", fromlist=["PrecisionFarming"]).PrecisionFarming()
    return await pf.get_climate_resilience_analysis(lat, lon, crop, farm_size, crop_value, yield_kg)


@router.get("/idle-land/{lat}/{lon}/{farm_size}")
async def check_idle_land(lat: float, lon: float, farm_size: float):
    from agriculture_intelligence.land_intelligence import LandIntelligence
    land = LandIntelligence()
    idle = await land.detect_idle_land_risk(lat, lon)
    from agriculture_intelligence.market_intelligence import MarketIntelligence
    mi = MarketIntelligence()
    opp = await mi.get_idle_land_opportunity(lat, lon, farm_size)
    return {"idle_risk": idle, "opportunity": opp}
