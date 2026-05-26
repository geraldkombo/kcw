import pytest
from services.risk_scoring import RiskScoringService
from services.securitisation import SecuritisationService
from models.risk import CreditAssessment


class TestRiskScoring:
    def setup_method(self):
        self.scorer = RiskScoringService()

    def test_pd_between_0_and_1(self):
        features = {
            "farm_size_ha": 2.0,
            "year_registered": 2022,
            "chama_member": 1,
            "sacco_member": 1,
            "mpesa_velocity": 5000,
            "gender_male": 0,
            "vegetation_index": 0.6,
            "moisture_stress": 0.3,
            "drought_risk": 0.1,
            "temp_anomaly": 0.0,
        }
        pd = self.scorer.predict_pd(features)
        assert 0 <= pd <= 1, f"PD {pd} outside [0, 1]"

    def test_high_risk_returns_high_pd(self):
        high_risk = {
            "farm_size_ha": 0.5,
            "year_registered": 2025,
            "chama_member": 0,
            "sacco_member": 0,
            "mpesa_velocity": 0,
            "gender_male": 1,
            "vegetation_index": 0.2,
            "moisture_stress": 0.8,
            "drought_risk": 0.9,
            "temp_anomaly": 1.5,
        }
        pd = self.scorer.predict_pd(high_risk)
        assert pd > 0.5, f"High risk PD {pd} should be > 0.5"

    def test_low_risk_returns_low_pd(self):
        low_risk = {
            "farm_size_ha": 5.0,
            "year_registered": 2020,
            "chama_member": 1,
            "sacco_member": 1,
            "mpesa_velocity": 50000,
            "gender_male": 0,
            "vegetation_index": 0.8,
            "moisture_stress": 0.1,
            "drought_risk": 0.05,
            "temp_anomaly": 0.0,
        }
        pd = self.scorer.predict_pd(low_risk)
        assert pd < 0.2, f"Low risk PD {pd} should be < 0.2"

    def test_sacco_member_decreases_risk(self):
        base = self.scorer.predict_pd({
            "farm_size_ha": 2.0, "year_registered": 2022,
            "chama_member": 0, "sacco_member": 0,
            "mpesa_velocity": 0, "gender_male": 1,
            "vegetation_index": 0.5, "moisture_stress": 0.3,
            "drought_risk": 0.2, "temp_anomaly": 0.0,
        })
        with_sacco = self.scorer.predict_pd({
            "farm_size_ha": 2.0, "year_registered": 2022,
            "chama_member": 0, "sacco_member": 1,
            "mpesa_velocity": 0, "gender_male": 1,
            "vegetation_index": 0.5, "moisture_stress": 0.3,
            "drought_risk": 0.2, "temp_anomaly": 0.0,
        })
        assert with_sacco < base, "SACCO membership should decrease PD"

    def test_score_to_rating(self):
        assert self.scorer.score_to_rating(85) == "A"
        assert self.scorer.score_to_rating(70) == "BBB"
        assert self.scorer.score_to_rating(55) == "BB"
        assert self.scorer.score_to_rating(40) == "B"
        assert self.scorer.score_to_rating(20) == "C"

    def test_risk_factors_sorted(self):
        features = {
            "farm_size_ha": 2.0, "year_registered": 2022,
            "chama_member": 1, "sacco_member": 1,
            "mpesa_velocity": 5000, "gender_male": 0,
            "vegetation_index": 0.6, "moisture_stress": 0.3,
            "drought_risk": 0.1, "temp_anomaly": 0.0,
        }
        factors = self.scorer.get_risk_factors(features)
        contributions = [abs(f["contribution"]) for f in factors]
        assert contributions == sorted(contributions, reverse=True)


class TestSecuritisation:
    def setup_method(self):
        self.service = SecuritisationService()

    def test_build_pool(self):
        farmers = [
            {"id": "KCW-001", "max_loan_kes": 18000, "probability_default": 0.12, "interest_rate_annual": 18.0, "loan_id": "LN-001"},
            {"id": "KCW-003", "max_loan_kes": 12000, "probability_default": 0.08, "interest_rate_annual": 16.0, "loan_id": "LN-004"},
            {"id": "KCW-004", "max_loan_kes": 45000, "probability_default": 0.05, "interest_rate_annual": 15.0, "loan_id": "LN-005"},
        ]
        pool = self.service.build_pool(farmers)
        assert pool.farmer_count == 3
        assert pool.total_notional_kes > 0
        assert 0 < pool.avg_pd < 1
        assert pool.expected_revenue_kes > pool.total_notional_kes  # includes interest

    def test_pool_excludes_high_risk(self):
        farmers = [
            {"id": "KCW-012", "max_loan_kes": 5000, "probability_default": 0.48, "interest_rate_annual": 25.0},
            {"id": "KCW-007", "max_loan_kes": 15000, "probability_default": 0.42, "interest_rate_annual": 24.0},
        ]
        pool = self.service.build_pool(farmers)
        assert pool.farmer_count == 0  # both above 0.35 threshold

    def test_pool_rating_inference(self):
        pool = self.service.build_pool([
            {"id": "KCW-010", "max_loan_kes": 22000, "probability_default": 0.03, "interest_rate_annual": 15.0},
            {"id": "KCW-013", "max_loan_kes": 80000, "probability_default": 0.02, "interest_rate_annual": 14.0},
        ])
        assert pool.target_rating == "A"

    def test_get_pool_nonexistent(self):
        assert self.service.get_pool("FAKE") is None

    def test_list_pools_empty(self):
        assert self.service.list_pools() == []

    def test_multiple_pools(self):
        pool_a = self.service.build_pool([
            {"id": "KCW-001", "max_loan_kes": 18000, "probability_default": 0.12, "interest_rate_annual": 18.0},
        ])
        pool_b = self.service.build_pool([
            {"id": "KCW-004", "max_loan_kes": 45000, "probability_default": 0.05, "interest_rate_annual": 15.0},
        ])
        pools = self.service.list_pools()
        assert len(pools) == 2
        assert pools[0] == pool_a.model_dump()
        assert pools[1] == pool_b.model_dump()
