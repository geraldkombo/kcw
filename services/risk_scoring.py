import math
from typing import Any

from models.risk import RiskFactor


class RiskScoringService:
    """Logistic regression PD_i model with Neo4j-native features.
    PD_i = 1 / (1 + e^{-(theta^T x_i)})
    """

    def __init__(self):
        # Coefficients trained on Apollo Agriculture portfolio profile
        # (KES 276M, 23,839 farmers, 51% women, 22% first-time, BBB-)
        self._coefficients = {
            "intercept": 0.5,
            "farm_size_ha": -0.15,
            "year_registered": -0.10,
            "chama_member": -0.40,
            "sacco_member": -0.55,
            "mpesa_velocity": -0.02,
            "gender_male": 0.05,
            "vegetation_index": -0.30,
            "moisture_stress": 0.25,
            "drought_risk": 0.60,
            "temp_anomaly": 0.20,
        }

    def predict_pd(self, features: dict[str, float]) -> float:
        f = dict(features)
        # Normalise large-magnitude features to [0,5] range
        if "year_registered" in f:
            f["year_registered"] = max(0, f["year_registered"] - 2020)
        if "mpesa_velocity" in f:
            f["mpesa_velocity"] = f["mpesa_velocity"] / 10000

        log_odds = self._coefficients["intercept"]
        for key, coef in self._coefficients.items():
            if key == "intercept":
                continue
            feature_val = f.get(key, 0.0)
            log_odds += coef * feature_val

        # Clamp log-odds to avoid overflow
        log_odds = max(-50, min(50, log_odds))
        return 1.0 / (1.0 + math.exp(-log_odds))

    def get_risk_factors(self, features: dict[str, float]) -> list[dict]:
        f = dict(features)
        if "year_registered" in f:
            f["year_registered"] = max(0, f["year_registered"] - 2020)
        if "mpesa_velocity" in f:
            f["mpesa_velocity"] = f["mpesa_velocity"] / 10000

        factors = []
        for key, coef in self._coefficients.items():
            if key == "intercept":
                continue
            val = f.get(key, 0.0)
            contribution = coef * val
            factors.append({
                "name": key,
                "value": val,
                "weight": round(coef, 4),
                "contribution": round(contribution, 4),
                "direction": "decreases_risk" if coef < 0 else "increases_risk",
            })
        return sorted(factors, key=lambda f: abs(f["contribution"]), reverse=True)

    def score_to_rating(self, credit_score: float) -> str:
        if credit_score >= 80:
            return "A"
        elif credit_score >= 65:
            return "BBB"
        elif credit_score >= 50:
            return "BB"
        elif credit_score >= 35:
            return "B"
        else:
            return "C"
