from __future__ import annotations

import uuid
from typing import Optional
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from api.dependencies import get_repository
from database.repository import Repository
from models.farmer import FarmerCreate, Farmer, FarmerStatus

router = APIRouter()


@router.get("")
async def list_farmers(
    county: Optional[str] = None,
    status: Optional[FarmerStatus] = None,
    limit: int = 100,
    repo: Repository = Depends(get_repository),
):
    farmers = repo.list_farmers()
    if county:
        farmers = [f for f in farmers if f.get("county", "").lower() == county.lower()]
    if status:
        status_val = status.value if isinstance(status, FarmerStatus) else status
        farmers = [f for f in farmers if f.get("status") == status_val]
    return farmers[:limit]


@router.post("", status_code=201)
async def create_farmer(data: FarmerCreate, repo: Repository = Depends(get_repository)):
    farmer_id = f"KCW-{uuid.uuid4().hex[:8].upper()}"
    farmer = Farmer(
        id=farmer_id,
        **data.model_dump(),
    )
    farmer_dict = farmer.model_dump()
    farmer_dict["farmer_id"] = farmer_id
    saved = repo.save_farmer(farmer_dict)
    return saved


@router.get("/{farmer_id}")
async def get_farmer(farmer_id: str, repo: Repository = Depends(get_repository)):
    farmer = repo.get_farmer(farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return farmer


@router.patch("/{farmer_id}")
async def update_farmer(farmer_id: str, updates: dict, repo: Repository = Depends(get_repository)):
    farmer = repo.get_farmer(farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    updated = {**farmer, **updates, "updated_at": datetime.now(timezone.utc).isoformat()}
    repo.save_farmer(updated)
    return updated
