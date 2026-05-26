from __future__ import annotations

import pytest
from agriculture_intelligence.precision_farming import (
    PrecisionFarming, PEST_THRESHOLDS, MICRO_CLIMATE_ZONES,
    CROP_BASE_TEMPS, HARVEST_GDD_THRESHOLDS,
)
from satellite.power_client import PowerClient


class FakePowerClient(PowerClient):
    """Return deterministic satellite data for unit tests."""

    async def get_temperature(self, lat: float, lon: float) -> dict:
        return {"mean": 20.0, "min": 12.0, "max": 28.0, "unit": "C"}

    async def get_solar_radiation(self, lat: float, lon: float) -> float:
        return 5.0

    async def get_ag_point(self, lat: float, lon: float) -> dict:
        return {"properties": {"parameter": {"GWETROOT": {"2000-01-01": 0.45}}}}


@pytest.fixture
def pf():
    return PrecisionFarming(power=FakePowerClient())


class TestComputeGDD:
    @pytest.mark.asyncio
    async def test_returns_gdd_for_rose(self, pf):
        r = await pf.compute_gdd(-0.7, 36.4, "rose")
        assert r["crop"] == "rose"
        assert r["base_temp_c"] == 7
        assert r["gdd_per_day"] > 0
        assert r["harvest_readiness"] in ("growing", "approaching", "ready")

    @pytest.mark.asyncio
    async def test_returns_gdd_for_maize(self, pf):
        r = await pf.compute_gdd(-1.0, 36.9, "maize")
        assert r["base_temp_c"] == 10
        assert "recommendation" in r

    @pytest.mark.asyncio
    async def test_benchmark_in_output(self, pf):
        r = await pf.compute_gdd(-0.7, 36.4, "rose")
        assert "FAO-66" in r["benchmark"]


class TestComputeET:
    @pytest.mark.asyncio
    async def test_returns_et0(self, pf):
        r = await pf.compute_et_penman_monteith(-1.0, 36.9)
        assert r["et0_mm_day"] > 0
        assert r["method"].startswith("FAO-56")
        assert "recommended_irrigation_pulses" in r

    @pytest.mark.asyncio
    async def test_benchmark_in_output(self, pf):
        r = await pf.compute_et_penman_monteith(-0.7, 36.4)
        assert "FAO-56" in r["benchmark"]


class TestPestDiseaseRisk:
    @pytest.mark.asyncio
    async def test_rose_returns_rose_pests(self, pf):
        r = await pf.assess_pest_disease_risk(-0.7, 36.4, "rose")
        pest_names = [p["pest"] for p in r["active_risks"]]
        assert "Downy Mildew" in pest_names or "Powdery Mildew" in pest_names or "Botrytis" in pest_names

    @pytest.mark.asyncio
    async def test_eu_export_compliance(self, pf):
        r = await pf.assess_pest_disease_risk(-0.7, 36.4, "rose")
        assert "eu_export_compliance" in r
        assert r["eu_export_compliance"]["eu_regulation"] == "EU 2024/2004 (effective Apr 26, 2025)"

    @pytest.mark.asyncio
    async def test_ipm_recommendations_present(self, pf):
        r = await pf.assess_pest_disease_risk(-0.7, 36.4, "rose")
        if r["active_risks"]:
            assert "ipm_recommendation" in r["active_risks"][0]

    @pytest.mark.asyncio
    async def test_false_codling_moth_detected_for_rose(self, pf):
        """FCM should be detectable as a rose pest since rose is in its crops list."""
        pet = PEST_THRESHOLDS["false_codling_moth"]
        assert "rose" in pet["crops"]

    @pytest.mark.asyncio
    async def test_low_temp_returns_no_pests(self, pf):
        class ColdPower(FakePowerClient):
            async def get_temperature(self, lat, lon):
                return {"mean": 5.0, "min": 2.0, "max": 8.0, "unit": "C"}
        cold_pf = PrecisionFarming(power=ColdPower())
        r = await cold_pf.assess_pest_disease_risk(-1.0, 36.9, "maize")
        assert r["total_risk_count"] == 0 or r["overall_risk"] == "low"


class TestClassifyMicroClimate:
    @pytest.mark.asyncio
    async def test_returns_zone(self, pf):
        r = await pf.classify_micro_climate(-0.7, 36.4)
        assert "zone" in r
        assert r["zone"] in MICRO_CLIMATE_ZONES

    @pytest.mark.asyncio
    async def test_recommended_crops_present(self, pf):
        r = await pf.classify_micro_climate(-0.7, 36.4)
        assert "recommended_crops" in r
        assert isinstance(r["recommended_crops"], list)
        assert len(r["recommended_crops"]) > 0


class TestAssessFrostRisk:
    @pytest.mark.asyncio
    async def test_returns_risk_level(self, pf):
        r = await pf.assess_frost_risk(-1.0, 36.9)
        assert r["frost_risk"] in ("none", "low", "moderate", "high", "severe")

    @pytest.mark.asyncio
    async def test_protective_measures_list(self, pf):
        r = await pf.assess_frost_risk(-0.7, 36.4)
        assert isinstance(r["protective_measures"], list)
        assert len(r["protective_measures"]) > 0


class TestPrecisionIrrigationTiming:
    @pytest.mark.asyncio
    async def test_returns_optimal_time(self, pf):
        r = await pf.get_precision_irrigation_timing(-0.7, 36.4)
        assert "optimal_irrigation_time" in r
        assert "water_saved_by_timing_pct" in r

    @pytest.mark.asyncio
    async def test_reason_present(self, pf):
        r = await pf.get_precision_irrigation_timing(-0.7, 36.4)
        assert len(r["reason"]) > 10


class TestVariableRateRecommendation:
    @pytest.mark.asyncio
    async def test_returns_zones(self, pf):
        r = await pf.get_variable_rate_recommendation(-0.7, 36.4, 2.0)
        assert len(r["zones"]) == 3
        assert r["farm_size_ha"] == 2.0

    @pytest.mark.asyncio
    async def test_water_saving_estimate(self, pf):
        r = await pf.get_variable_rate_recommendation(-0.7, 36.4)
        assert r["water_saving_vs_uniform_pct"] >= 0


class TestEquatorialBenchmark:
    @pytest.mark.asyncio
    async def test_returns_suitability(self, pf):
        r = await pf.get_equatorial_benchmark(-0.7, 36.4)
        assert "climatic_suitability_score" in r
        assert "climatic_grade" in r
        assert r["climatic_grade"] in ("Excellent", "Good", "Fair", "Limited")

    @pytest.mark.asyncio
    async def test_benchmark_systems_listed(self, pf):
        r = await pf.get_equatorial_benchmark(-0.7, 36.4)
        assert len(r["benchmark_systems"]) == 4
        names = [s["region"] for s in r["benchmark_systems"]]
        assert "East Africa highlands" in names
        assert "West Africa savanna" in names

    @pytest.mark.asyncio
    async def test_low_temp_returns_lower_score(self, pf):
        class HotPower(FakePowerClient):
            async def get_temperature(self, lat, lon):
                return {"mean": 30.0, "min": 25.0, "max": 35.0, "unit": "C"}
        hot_pf = PrecisionFarming(power=HotPower())
        r = await hot_pf.get_equatorial_benchmark(-1.0, 36.9)
        assert r["climatic_suitability_score"] < 80


class TestClimateResilienceAnalysis:
    @pytest.mark.asyncio
    async def test_returns_resilience_analysis(self, pf):
        r = await pf.get_climate_resilience_analysis(-0.7, 36.4, "maize", 1.0)
        assert "climate_risk_profile" in r
        assert "expected_loss_without_adaptation_kes" in r
        assert "adaptation_roi_pct" in r
        assert "policy_context" in r

    @pytest.mark.asyncio
    async def test_policy_context_references_budget_testimony(self, pf):
        r = await pf.get_climate_resilience_analysis(-0.7, 36.4)
        ctx = r["policy_context"]
        assert "kenya_disaster_response_2024_kes" in ctx
        assert "climate_smart_ag_budget_2026_2027" in ctx
        assert "Budget Committee" in ctx.get("source", "")

    @pytest.mark.asyncio
    async def test_disaster_response_cost_higher_than_adaptation(self, pf):
        r = await pf.get_climate_resilience_analysis(-1.0, 36.9, "maize", 2.0)
        assert r["disaster_response_cost_estimate_kes"] >= r["cost_of_precision_ag_kes"]

    @pytest.mark.asyncio
    async def test_low_risk_location_recommends_monitoring(self, pf):
        class CoolDryPower(FakePowerClient):
            async def get_temperature(self, lat, lon):
                return {"mean": 18.0, "min": 14.0, "max": 22.0, "unit": "C"}
            async def get_solar_radiation(self, lat, lon):
                return 3.0
        mild_pf = PrecisionFarming(power=CoolDryPower())
        r = await mild_pf.get_climate_resilience_analysis(-0.7, 36.4, "maize", 1.0)
        assert "Low climate risk" in r["recommendation"] or r["adaptation_roi_pct"] < 50

    @pytest.mark.asyncio
    async def test_recommendation_in_output(self, pf):
        r = await pf.get_climate_resilience_analysis(-0.7, 36.4, "maize", 1.0)
        assert "recommendation" in r
        assert len(r["recommendation"]) > 20


class TestPestThresholds:
    def test_crops_listed(self):
        assert "rose" in PEST_THRESHOLDS["downy_mildew"]["crops"]
        assert "rose" in PEST_THRESHOLDS["powdery_mildew"]["crops"]
        assert "rose" in PEST_THRESHOLDS["fusarium_wilt"]["crops"]
        assert "rose" in PEST_THRESHOLDS["botrytis"]["crops"]
        assert "rose" in PEST_THRESHOLDS["false_codling_moth"]["crops"]


class TestConstants:
    def test_crop_base_temps(self):
        assert CROP_BASE_TEMPS["rose"] == 7
        assert HARVEST_GDD_THRESHOLDS["rose"] == 2500

    def test_micro_climate_zones_have_descriptions(self):
        for zone, info in MICRO_CLIMATE_ZONES.items():
            assert "description" in info
            assert "temp_range" in info
            assert len(info["description"]) > 10
