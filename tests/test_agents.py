import pytest
from agents.orchestrator import OrchestratorAgent
from agents.onboarding_agent import OnboardingAgent
from agents.credit_agent import CreditAssessmentAgent
from agents.geo_audit_agent import GeoAuditAgent
from agents.macro_climatic_agent import MacroClimaticAgent
from agents.verification_agent import VerificationAgent
from agents.procurement_agent import ProcurementAgent
from agents.liquidity_agent import LiquidityAgent
from services.risk_scoring import RiskScoringService
from services.securitisation import SecuritisationService


class TestOnboardingAgent:
    @pytest.mark.asyncio
    async def test_ingest_creates_profile(self):
        agent = OnboardingAgent()
        profile = await agent.ingest({
            "first_name": "Grace", "last_name": "Wanjiku",
            "phone": "+254712345001", "county": "Kiambu", "gender": "F",
            "latitude": -1.0, "longitude": 36.9, "farm_size_ha": 2.5,
            "primary_crop": "maize", "chama_member": True,
        })
        assert profile["first_name"] == "Grace"
        assert profile["county"] == "Kiambu"
        assert profile["farm_size_ha"] == 2.5

    @pytest.mark.asyncio
    async def test_ingest_handles_raw_text_without_llm(self):
        agent = OnboardingAgent()
        profile = await agent.ingest({"raw_text": "Nataka mkopo ya mbegu", "source_language": "sw"})
        assert profile["id"].startswith("KCW-")
        assert profile["source_language"] == "sw"


class TestGeoAuditAgent:
    @pytest.mark.asyncio
    async def test_audit_returns_report(self):
        agent = GeoAuditAgent()
        report = await agent.audit({"latitude": -1.0, "longitude": 36.9, "county": "Kiambu"})
        assert "vegetation_index" in report
        assert "moisture_stress" in report
        assert report["geo_verified"] is True

    @pytest.mark.asyncio
    async def test_audit_different_counties(self):
        agent = GeoAuditAgent()
        machakos = await agent.audit({"latitude": -1.5, "longitude": 37.3, "county": "Machakos"})
        kisumu = await agent.audit({"latitude": -0.1, "longitude": 34.75, "county": "Kisumu"})
        # Both should return valid vegetation_index values (may be same at 0.5deg grid resolution)
        assert 0.0 <= machakos["vegetation_index"] <= 1.0
        assert 0.0 <= kisumu["vegetation_index"] <= 1.0
        assert "nasa_power" in machakos.get("data_source", "")
        assert "soil_quality" in machakos
        assert "solar_radiation_kwh_m2_day" in machakos


class TestMacroClimaticAgent:
    @pytest.mark.asyncio
    async def test_assess_returns_climate_data(self):
        agent = MacroClimaticAgent()
        report = await agent.assess({"county": "Machakos", "latitude": -1.5, "longitude": 37.3})
        assert "drought_risk" in report
        assert "temp_anomaly" in report
        assert "climate_zone" in report

    @pytest.mark.asyncio
    async def test_drought_risk_variation(self):
        agent = MacroClimaticAgent()
        dry = await agent.assess({"county": "Machakos", "latitude": -1.5, "longitude": 37.3})
        wet = await agent.assess({"county": "Kisumu", "latitude": -0.1, "longitude": 34.75})
        assert dry["drought_risk"] > wet["drought_risk"]


class TestVerificationAgent:
    @pytest.mark.asyncio
    async def test_passes_valid_data(self):
        agent = VerificationAgent()
        result = await agent.verify(
            farmer_profile={"id": "KCW-001", "county": "Kiambu", "latitude": -1.0, "farm_size_ha": 2.5},
            geo_report={"vegetation_index": 0.6},
            climate_report={"drought_risk": 0.1},
            assessment={"probability_default": 0.12, "max_loan_kes": 20000},
        )
        assert result["passed"] is True
        assert len(result["inconsistencies"]) == 0

    @pytest.mark.asyncio
    async def test_fails_invalid_latitude(self):
        agent = VerificationAgent()
        result = await agent.verify(
            farmer_profile={"id": "KCW-999", "county": "Nairobi", "latitude": -15.0, "farm_size_ha": 1.0},
            geo_report={"vegetation_index": 0.5},
            climate_report={"drought_risk": 0.3},
            assessment={"probability_default": 0.5, "max_loan_kes": 5000},
        )
        assert result["passed"] is False

    @pytest.mark.asyncio
    async def test_produces_verification_hash(self):
        agent = VerificationAgent()
        result = await agent.verify(
            farmer_profile={"id": "KCW-001", "latitude": -1.0, "county": "Kiambu", "farm_size_ha": 2.0},
            geo_report={"vegetation_index": 0.6},
            climate_report={"drought_risk": 0.1},
            assessment={"probability_default": 0.1, "max_loan_kes": 20000},
        )
        assert len(result["verification_hash"]) == 64
        assert result["verified_by"] == "kcw-vv-agent-v1"


class TestCreditAssessmentAgent:
    def setup_method(self):
        self.agent = CreditAssessmentAgent(risk_scorer=RiskScoringService())

    @pytest.mark.asyncio
    async def test_assess_low_risk_farmer(self):
        result = await self.agent.assess(
            farmer_profile={"id": "KCW-010", "farm_size_ha": 1.8, "year_registered": 2021,
                            "chama_member": True, "sacco_member": True, "gender": "F",
                            "mpesa_monthly_velocity": 15000},
            geo_report={"vegetation_index": 0.7, "moisture_stress": 0.2},
            climate_report={"drought_risk": 0.05, "temp_anomaly": 0.0},
        )
        assert 0 <= result["probability_default"] <= 1
        assert 0 <= result["credit_score"] <= 100
        assert result["approved"] is True

    @pytest.mark.asyncio
    async def test_assess_high_risk_farmer(self):
        result = await self.agent.assess(
            farmer_profile={"id": "KCW-012", "farm_size_ha": 0.8, "year_registered": 2023,
                            "chama_member": True, "sacco_member": False, "gender": "F",
                            "mpesa_monthly_velocity": 500},
            geo_report={"vegetation_index": 0.2, "moisture_stress": 0.7},
            climate_report={"drought_risk": 0.8, "temp_anomaly": 1.2},
        )
        if result["probability_default"] > 0.35:
            assert result["approved"] is False


class TestOrchestrator:
    @pytest.mark.asyncio
    async def test_process_farmer_application(self):
        orchestrator = OrchestratorAgent(
            onboarding=OnboardingAgent(),
            credit=CreditAssessmentAgent(risk_scorer=RiskScoringService()),
            geo=GeoAuditAgent(),
            climatic=MacroClimaticAgent(),
            verification=VerificationAgent(),
            procurement=ProcurementAgent(),
            liquidity=LiquidityAgent(securitisation=SecuritisationService()),
        )
        result = await orchestrator.process_farmer_application({
            "first_name": "Faith", "last_name": "Njeri",
            "phone": "+254712345010", "county": "Nyeri", "gender": "F",
            "latitude": -0.28, "longitude": 36.95, "farm_size_ha": 1.8,
            "primary_crop": "tea", "chama_member": True, "sacco_member": True,
        })
        assert "workflow_id" in result
        assert result["status"] in ("approved", "declined")
