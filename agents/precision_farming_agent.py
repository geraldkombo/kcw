"""Precision farming agent — equatorial general agriculture intelligence.
Operates at the standard of the world's best farms across all crop types."""

from __future__ import annotations

from agriculture_intelligence.precision_farming import PrecisionFarming
from satellite.power_client import PowerClient


class PrecisionFarmingAgent:
    """Agent delivering equatorial precision farming intelligence for any crop."""

    def __init__(self, power: PowerClient | None = None):
        self.pf = PrecisionFarming(power or PowerClient())

    async def analyze(self, latitude: float, longitude: float, crop: str = "maize",
                      farm_size_ha: float = 1.0) -> dict:
        """Full precision farming analysis — GDD, ET, pest risk, micro-climate, frost, timing."""
        gdd = await self.pf.compute_gdd(latitude, longitude, crop)
        et = await self.pf.compute_et_penman_monteith(latitude, longitude)
        pest = await self.pf.assess_pest_disease_risk(latitude, longitude, crop)
        climate = await self.pf.classify_micro_climate(latitude, longitude)
        frost = await self.pf.assess_frost_risk(latitude, longitude)
        timing = await self.pf.get_precision_irrigation_timing(latitude, longitude)
        vrate = await self.pf.get_variable_rate_recommendation(latitude, longitude, farm_size_ha)
        equatorial_benchmark = await self.pf.get_equatorial_benchmark(latitude, longitude)
        resilience = await self.pf.get_climate_resilience_analysis(latitude, longitude, crop, farm_size_ha)

        return {
            "location": {"latitude": latitude, "longitude": longitude, "crop": crop},
            "growing_degree_days": gdd,
            "evapotranspiration": et,
            "pest_disease_risk": pest,
            "micro_climate": climate,
            "frost_risk": frost,
            "precision_irrigation_timing": timing,
            "variable_rate_recommendation": vrate,
            "equatorial_benchmark": equatorial_benchmark,
            "climate_resilience_analysis": resilience,
            "overall_precision_grade": self._grade(gdd, et, pest, frost),
        }

    def _grade(self, gdd: dict, et: dict, pest: dict, frost: dict) -> str:
        if frost.get("frost_risk") in ("severe", "high"):
            return "C — frost risk requires protective measures"
        if pest.get("overall_risk") == "high":
            return "B — pest pressure elevated, consider integrated pest management"
        if gdd.get("harvest_readiness") == "ready":
            return "A — optimal, harvest window open"
        return "A — conditions favourable for precision management"
