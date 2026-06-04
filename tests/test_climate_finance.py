from __future__ import annotations

import pytest
from knowledge.climate_finance import ClimateFinanceKnowledge


@pytest.fixture
def cfk():
    return ClimateFinanceKnowledge()


class TestParametricInsurance:
    def test_model_structure(self, cfk):
        m = cfk.PARAMETRIC_INSURANCE_MODEL
        assert "trigger_metrics" in m
        assert len(m["trigger_metrics"]) == 3
        names = {t["name"] for t in m["trigger_metrics"]}
        assert names == {"rainfall_deficit", "land_surface_temperature", "vegetation_index_anomaly"}

    def test_regulatory_context(self, cfk):
        ctx = cfk.PARAMETRIC_INSURANCE_MODEL["regulatory_context"]
        assert "Insurance Regulatory Authority of Kenya (IRA)" in ctx["regulator"]
        assert "10 days" in ctx["kenya_2026_proposal"]

    def test_target_crops_includes_indigenous(self, cfk):
        targets = cfk.PARAMETRIC_INSURANCE_MODEL["target_crops"]
        assert "amaranth" in targets
        assert "sorghum" in targets
        assert "dek" in targets

    def test_county_profile_homa_bay(self, cfk):
        p = cfk._get_county_risk_profile("homa bay")
        assert p["primary_risk"] == "Flooding (Lake Victoria basin) + drought"
        assert "high" in p["parametric_suitability"]

    def test_county_profile_kitui(self, cfk):
        p = cfk._get_county_risk_profile("kitui")
        assert "Drought" in p["primary_risk"]

    def test_county_profile_none(self, cfk):
        p = cfk._get_county_risk_profile(None)
        assert "note" in p


class TestGreenBond:
    def test_framework_structure(self, cfk):
        gb = cfk.GREEN_BOND_FRAMEWORK
        assert "$772M" in gb["description"]
        assert len(gb["allocations"]) == 4

    def test_allocations_sum_to_100(self, cfk):
        total = sum(a["allocation_pct"] for a in cfk.GREEN_BOND_FRAMEWORK["allocations"])
        assert total == 100

    def test_instruments(self, cfk):
        assert "5-year green bond" in cfk.GREEN_BOND_FRAMEWORK["instruments"]
        assert "10-year green bond" in cfk.GREEN_BOND_FRAMEWORK["instruments"]


class TestUSAIDImpact:
    def test_key_metrics_present(self, cfk):
        km = cfk.USAID_FREEZE_IMPACT["key_metrics"]
        assert "$225M" in km["bilateral_aid_contraction_usd"]
        assert km["award_termination_rate_pct"] == "70–86"

    def test_systemic_consequence(self, cfk):
        sc = cfk.USAID_FREEZE_IMPACT["systemic_consequence"]
        assert "zero external inputs" in sc
        assert "cultural preference" in sc


class TestPHL:
    def test_phl_rate(self, cfk):
        assert cfk.POST_HARVEST_LOSS_DATA["aiv_phl_rate_pct"] == 57

    def test_interventions(self, cfk):
        interventions = cfk.POST_HARVEST_LOSS_DATA["interventions"]
        assert len(interventions) == 2
        assert interventions[0]["phl_reduction_pct"] == 45


class TestCarbonCredits:
    def test_sequestration_data(self, cfk):
        seq = cfk.CARBON_CREDIT_POTENTIAL["estimated_sequestration_tonnes_co2_per_ha"]
        assert seq["sorghum_cowpea_intercrop"] == 2.5
        assert seq["maize_monoculture_reference"] == -0.5

    def test_standards(self, cfk):
        assert "Verra (VCS)" in cfk.CARBON_CREDIT_POTENTIAL["standards"]
        assert "Plan Vivo (for smallholders)" in cfk.CARBON_CREDIT_POTENTIAL["standards"]


class TestDeRiskOverview:
    def test_four_forces(self, cfk):
        overview = cfk.get_de_risk_overview()
        assert len(overview["forces"]) == 4
        names = [f["name"] for f in overview["forces"]]
        assert "Climate crisis" in names
        assert "Funding collapse" in names
        assert "Innovation maturity" in names
        assert "Knowledge validation" in names

    def test_verdict(self, cfk):
        overview = cfk.get_de_risk_overview()
        assert "idea whose time has come" in overview["verdict"].lower()


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from api.main import app
    return TestClient(app)


class TestAPIEndpoints:
    def test_overview_endpoint(self, client):
        resp = client.get("/api/v1/de-risk/overview")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["forces"]) == 4

    def test_parametrics_endpoint(self, client):
        resp = client.get("/api/v1/de-risk/parametrics")
        assert resp.status_code == 200
        data = resp.json()
        assert "model" in data
        assert "county_context" in data

    def test_parametrics_with_county(self, client):
        resp = client.get("/api/v1/de-risk/parametrics?county=homa+bay")
        assert resp.status_code == 200
        data = resp.json()
        assert data["county_context"]["primary_risk"] == "Flooding (Lake Victoria basin) + drought"

    def test_green_bond_endpoint(self, client):
        resp = client.get("/api/v1/de-risk/green-bond")
        assert resp.status_code == 200
        data = resp.json()
        assert "$772M" in data["description"]

    def test_usaid_endpoint(self, client):
        resp = client.get("/api/v1/de-risk/usaid-impact")
        assert resp.status_code == 200
        data = resp.json()
        assert "$225M" in data["key_metrics"]["bilateral_aid_contraction_usd"]

    def test_phl_endpoint(self, client):
        resp = client.get("/api/v1/de-risk/post-harvest-loss")
        assert resp.status_code == 200
        data = resp.json()
        assert data["aiv_phl_rate_pct"] == 57

    def test_carbon_endpoint(self, client):
        resp = client.get("/api/v1/de-risk/carbon-credits")
        assert resp.status_code == 200
        data = resp.json()
        seq = data["estimated_sequestration_tonnes_co2_per_ha"]
        assert seq["sorghum_cowpea_intercrop"] == 2.5

    def test_marketplace_de_risk(self, client):
        create = client.post("/api/v1/marketplace/listings", json={
            "food": "amaranth",
            "county": "homa bay",
            "seller": "Test",
            "quantity_kg": 50,
            "price_kes_per_kg": 120,
        })
        assert create.status_code == 200
        lid = create.json()["id"]
        resp = client.get(f"/api/v1/marketplace/listings/{lid}/de-risk")
        assert resp.status_code == 200
        data = resp.json()
        assert data["resilience_score"] is not None
        assert "parametric_insurance" in data
        assert "post_harvest_loss" in data
