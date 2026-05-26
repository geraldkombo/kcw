from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum


class LoanStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    disbursed = "disbursed"
    active = "active"
    repaid = "repaid"
    defaulted = "defaulted"


class LoanPurpose(str, Enum):
    seeds = "seeds"
    fertiliser = "fertiliser"
    equipment = "equipment"
    irrigation = "irrigation"
    livestock = "livestock"
    transport = "transport"
    processing = "processing"
    other = "other"


class LoanCreate(BaseModel):
    farmer_id: str
    amount_kes: float = Field(..., gt=0, le=500000)
    purpose: LoanPurpose
    term_months: int = Field(..., ge=1, le=24)
    interest_rate_annual: float = Field(..., ge=0, le=100)
    disbursement_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    farm_size_ha: Optional[float] = None
    year_registered: Optional[int] = None
    chama_member: Optional[bool] = None
    sacco_member: Optional[bool] = None
    mpesa_velocity: Optional[float] = None
    gender: Optional[str] = None
    vegetation_index: Optional[float] = None
    moisture_stress: Optional[float] = None
    drought_risk: Optional[float] = None
    temp_anomaly: Optional[float] = None


class Loan(LoanCreate):
    id: str
    status: LoanStatus = LoanStatus.pending
    pd_at_origination: Optional[float] = None
    credit_score_at_origination: Optional[float] = None
    amount_repaid_kes: float = 0.0
    agent_decision_trace: Optional[dict] = None
    masumi_escrow_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(from_attributes=True)
