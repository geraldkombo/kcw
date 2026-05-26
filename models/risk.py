from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Optional


class RiskFactor(BaseModel):
    name: str
    value: float
    weight: float
    source: str


class CreditAssessment(BaseModel):
    farmer_id: str
    loan_id: str
    probability_default: float = Field(..., ge=0, le=1)
    credit_score: float = Field(..., ge=0, le=100)
    risk_factors: list[RiskFactor] = Field(default_factory=list)
    agent_used: str
    model_version: str = "kcw-logistic-v1"
    verification_hash: str
    neo4j_trace_id: str
    assessed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class VerificationResult(BaseModel):
    passed: bool
    checks: list[dict]
    inconsistencies: list[str] = Field(default_factory=list)
    verified_by: str
    verified_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
