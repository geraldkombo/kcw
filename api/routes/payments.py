from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from masumi.x402_client import MasumiX402Client
from masumi.escrow_lifecycle import EscrowLifecycle, EscrowState
from api.dependencies import get_masumi

router = APIRouter()

# In-memory escrow tracker
_escrows: dict[str, EscrowLifecycle] = {}


class CreatePaymentRequest(BaseModel):
    amount_lovelace: int
    description: str


class SubmitResultRequest(BaseModel):
    result_hash: str


class RefundRequest(BaseModel):
    reason: str


@router.post("/escrow", status_code=201)
async def create_escrow(req: CreatePaymentRequest):
    escrow_id = f"ESC-{__import__('uuid').uuid4().hex[:12].upper()}"
    lifecycle = EscrowLifecycle(escrow_id=escrow_id)
    _escrows[escrow_id] = lifecycle
    return {
        "escrow_id": escrow_id,
        "state": lifecycle.state.value,
        "amount_lovelace": req.amount_lovelace,
        "description": req.description,
    }


@router.get("/escrow/{escrow_id}")
async def get_escrow(escrow_id: str):
    escrow = _escrows.get(escrow_id)
    if not escrow:
        raise HTTPException(status_code=404, detail="Escrow not found")
    return escrow.to_dict()


@router.post("/escrow/{escrow_id}/confirm")
async def confirm_escrow(escrow_id: str):
    escrow = _escrows.get(escrow_id)
    if not escrow:
        raise HTTPException(status_code=404, detail="Escrow not found")
    try:
        escrow.state = EscrowState.FUNDS_LOCKED
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return escrow.to_dict()


@router.post("/escrow/{escrow_id}/submit-result")
async def submit_result(escrow_id: str, req: SubmitResultRequest):
    escrow = _escrows.get(escrow_id)
    if not escrow:
        raise HTTPException(status_code=404, detail="Escrow not found")
    try:
        escrow.state = EscrowState.RESULT_SUBMITTED
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        **escrow.to_dict(),
        "result_hash": req.result_hash,
    }


@router.post("/escrow/{escrow_id}/complete")
async def complete_escrow(escrow_id: str):
    escrow = _escrows.get(escrow_id)
    if not escrow:
        raise HTTPException(status_code=404, detail="Escrow not found")
    try:
        escrow.state = EscrowState.COMPLETED
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return escrow.to_dict()


@router.post("/escrow/{escrow_id}/refund")
async def request_refund(escrow_id: str, req: RefundRequest):
    escrow = _escrows.get(escrow_id)
    if not escrow:
        raise HTTPException(status_code=404, detail="Escrow not found")
    try:
        escrow.state = EscrowState.REFUND_REQUESTED
        escrow.state = EscrowState.REFUNDED
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {**escrow.to_dict(), "reason": req.reason}


@router.get("/x402/status")
async def x402_status(
    masumi: MasumiX402Client = Depends(get_masumi),
):
    return {
        "network": masumi.network,
        "wallet": masumi.wallet_address[:15] + "...",
        "configured": bool(masumi.wallet_address),
    }
