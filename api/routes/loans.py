from __future__ import annotations

import uuid
from typing import Optional
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Depends

from api.dependencies import get_repository, get_audit
from database.repository import Repository
from models.loan import LoanCreate, Loan, LoanStatus
from services.risk_scoring import RiskScoringService
from services.reporting import AuditTrail

router = APIRouter()

_risk_scorer = RiskScoringService()


@router.get("")
async def list_loans(
    farmer_id: Optional[str] = None,
    status: Optional[LoanStatus] = None,
    limit: int = 100,
    repo: Repository = Depends(get_repository),
):
    loans = repo.list_loans()
    if farmer_id:
        loans = [l for l in loans if l.get("farmer_id") == farmer_id]
    if status:
        status_val = status.value if isinstance(status, LoanStatus) else status
        loans = [l for l in loans if l.get("status") == status_val]
    return loans[:limit]


@router.post("", status_code=201)
async def create_loan(
    data: LoanCreate,
    repo: Repository = Depends(get_repository),
    audit: AuditTrail = Depends(get_audit),
):
    loan_id = f"LN-{uuid.uuid4().hex[:8].upper()}"

    features = {
        "farm_size_ha": data.farm_size_ha or 2.0,
        "year_registered": data.year_registered or 2022,
        "chama_member": 1 if data.chama_member else 0,
        "sacco_member": 1 if data.sacco_member else 0,
        "mpesa_velocity": data.mpesa_velocity or 0,
        "gender_male": 1 if (data.gender or "M") == "M" else 0,
        "vegetation_index": data.vegetation_index or 0.5,
        "moisture_stress": data.moisture_stress or 0.3,
        "drought_risk": data.drought_risk or 0.2,
        "temp_anomaly": data.temp_anomaly or 0.0,
    }

    pd_value = _risk_scorer.predict_pd(features)

    loan = Loan(
        id=loan_id,
        **data.model_dump(),
        pd_at_origination=round(pd_value, 4),
        credit_score_at_origination=round((1 - pd_value) * 100, 1),
    )
    loan_dict = loan.model_dump()
    loan_dict["loan_id"] = loan_id
    saved = repo.save_loan(loan_dict)
    return saved


@router.get("/{loan_id}")
async def get_loan(loan_id: str, repo: Repository = Depends(get_repository)):
    loan = repo.get_loan(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan


@router.patch("/{loan_id}/status")
async def update_loan_status(loan_id: str, status: LoanStatus, repo: Repository = Depends(get_repository)):
    loan = repo.get_loan(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    loan["status"] = status.value if isinstance(status, LoanStatus) else status
    loan["updated_at"] = datetime.now(timezone.utc).isoformat()
    repo.save_loan(loan)
    return loan
