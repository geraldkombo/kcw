from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum


class Gender(str, Enum):
    male = "M"
    female = "F"


class FarmerStatus(str, Enum):
    active = "active"
    delinquent = "delinquent"
    defaulted = "defaulted"
    completed = "completed"


class FarmerCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., pattern=r"^\+?\d{9,15}$")
    gender: Gender
    county: str
    sub_county: str
    village: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    farm_size_ha: float = Field(..., gt=0)
    primary_crop: str
    year_registered: int = Field(..., ge=2020, le=2026)
    chama_member: bool = False
    sacco_member: bool = False
    has_mpesa_account: bool = True


class Farmer(FarmerCreate):
    id: str
    status: FarmerStatus = FarmerStatus.active
    credit_score: Optional[float] = None
    probability_default: Optional[float] = None
    total_loans_taken: int = 0
    total_loans_repaid: int = 0
    total_borrowed_kes: float = 0.0
    total_repaid_kes: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(from_attributes=True)
