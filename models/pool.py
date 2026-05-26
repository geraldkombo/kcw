from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum


class PoolStatus(str, Enum):
    assembling = "assembling"
    rated = "rated"
    subscribed = "subscribed"
    settled = "settled"
    closed = "closed"


class TrancheClass(str, Enum):
    senior = "senior"
    mezzanine = "mezzanine"
    junior = "junior"


class SecuritisationPool(BaseModel):
    id: str
    name: str
    status: PoolStatus = PoolStatus.assembling
    loan_ids: list[str] = Field(default_factory=list)
    total_notional_kes: float = 0.0
    farmer_count: int = 0
    avg_pd: float = 0.0
    expected_revenue_kes: float = 0.0
    target_rating: str = "BBB-"
    anchor_investor: Optional[str] = None
    first_loss_pct: float = 0.0
    senior_pct: float = 70.0
    mezzanine_pct: float = 20.0
    junior_pct: float = 10.0
    masumi_pool_contract_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(from_attributes=True)
