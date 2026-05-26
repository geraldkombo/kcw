from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.securitisation import SecuritisationService
from api.dependencies import get_securitisation

router = APIRouter()


class BuildPoolRequest(BaseModel):
    farmer_data: list[dict]


@router.get("")
async def list_pools(
    securitisation: SecuritisationService = Depends(get_securitisation),
):
    return securitisation.list_pools()


@router.post("/build", status_code=201)
async def build_pool(
    req: BuildPoolRequest,
    securitisation: SecuritisationService = Depends(get_securitisation),
):
    if not req.farmer_data:
        raise HTTPException(status_code=400, detail="No farmers provided")

    pool = securitisation.build_pool(req.farmer_data)
    return pool.model_dump()


@router.get("/{pool_id}")
async def get_pool(
    pool_id: str,
    securitisation: SecuritisationService = Depends(get_securitisation),
):
    pool = securitisation.get_pool(pool_id)
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")
    return pool
