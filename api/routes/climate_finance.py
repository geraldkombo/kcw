from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Query

from knowledge.climate_finance import ClimateFinanceKnowledge

router = APIRouter(prefix="/api/v1/de-risk", tags=["Climate Finance & De-risking"])

_cfk = ClimateFinanceKnowledge()


@router.get("/overview")
async def de_risk_overview():
    """Unified de-risking framework — the four forces making traditional food systems investable."""
    return _cfk.get_de_risk_overview()


@router.get("/parametrics")
async def parametric_insurance(county: Optional[str] = Query(None, description="Filter risk profile by county")):
    """Satellite-triggered parametric insurance model for indigenous crops."""
    return _cfk.get_parametrics(county)


@router.get("/green-bond")
async def green_bond_framework():
    """Kenya's $772M sovereign green bond for climate-smart agriculture."""
    return _cfk.get_green_bond_summary()


@router.get("/usaid-impact")
async def usaid_freeze_impact():
    """USAID Executive Order 14169 — funding contraction and systemic consequences."""
    return _cfk.get_usaid_impact()


@router.get("/post-harvest-loss")
async def post_harvest_loss():
    """57% post-harvest loss rate for AIVs and mitigation interventions."""
    return _cfk.get_phl_analysis()


@router.get("/carbon-credits")
async def carbon_credit_potential():
    """Carbon sequestration potential of traditional intercropping systems."""
    return _cfk.get_carbon_potential()
