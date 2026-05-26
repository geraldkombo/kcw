import json
from typing import Optional

from models.risk import RiskFactor
from services.risk_scoring import RiskScoringService
from featherless.client import FeatherlessClient


class CreditAssessmentAgent:
    """Credit Assessment Agent — computes PD_i via logistic regression
    augmented by DeepSeek V4 Pro reasoning over Neo4j graph features.
    """

    def __init__(
        self,
        risk_scorer: RiskScoringService,
        featherless: Optional[FeatherlessClient] = None,
    ):
        self.risk_scorer = risk_scorer
        self.featherless = featherless

    async def assess(
        self,
        farmer_profile: dict,
        geo_report: dict,
        climate_report: dict,
    ) -> dict:
        features = self._build_features(farmer_profile, geo_report, climate_report)

        # Logistic regression PD
        pd_value = self.risk_scorer.predict_pd(features)
        credit_score = max(0, min(100, round((1 - pd_value) * 100, 1)))

        assessment = {
            "farmer_id": farmer_profile.get("id"),
            "probability_default": round(pd_value, 4),
            "credit_score": credit_score,
            "approved": pd_value < 0.35,
            "max_loan_kes": self._compute_max_loan(
                pd_value, farmer_profile
            ),
            "risk_factors": self.risk_scorer.get_risk_factors(features),
            "model": "kcw-logistic-v1",
        }

        # Augment with LLM reasoning if Featherless available
        if self.featherless:
            llm_assessment = await self.featherless.credit_assessment(
                farmer_data={
                    **farmer_profile,
                    "geo_report": geo_report,
                    "climate_report": climate_report,
                    "model_pd": pd_value,
                },
                prompt="Assess this farmer's creditworthiness considering "
                "the graph-derived PD, geo-spatial data, and climate stress.",
            )
            if isinstance(llm_assessment, str):
                try:
                    llm_assessment = json.loads(llm_assessment)
                except json.JSONDecodeError:
                    pass
            if isinstance(llm_assessment, dict):
                assessment["llm_reasoning"] = llm_assessment.get("reasoning", "")
                assessment["risk_factors"].extend(
                    llm_assessment.get("risk_factors", [])
                )

        return assessment

    def _build_features(
        self, farmer: dict, geo: dict, climate: dict
    ) -> dict:
        return {
            "farm_size_ha": farmer.get("farm_size_ha", 1.0),
            "year_registered": farmer.get("year_registered", 2025),
            "chama_member": int(farmer.get("chama_member", False)),
            "sacco_member": int(farmer.get("sacco_member", False)),
            "mpesa_velocity": farmer.get("mpesa_monthly_velocity", 0),
            "gender_male": 1 if farmer.get("gender") == "M" else 0,
            "vegetation_index": geo.get("vegetation_index", 0.5),
            "moisture_stress": geo.get("moisture_stress", 0.3),
            "drought_risk": climate.get("drought_risk", 0.2),
            "temp_anomaly": climate.get("temp_anomaly", 0.0),
        }

    def _compute_max_loan(self, pd: float, farmer: dict) -> float:
        base = farmer.get("farm_size_ha", 1.0) * 12000
        if farmer.get("sacco_member"):
            base *= 1.3
        if farmer.get("chama_member"):
            base *= 1.15
        risk_multiplier = max(0.3, 1 - pd * 2)
        return round(base * risk_multiplier, -2)
