from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Query

from agriculture_intelligence.market_intelligence import MarketIntelligence
from knowledge.climate_finance import ClimateFinanceKnowledge
from knowledge.traditional_foods import TraditionalFoodsIndex

logger = logging.getLogger("frk.marketplace")
router = APIRouter(prefix="/api/v1/marketplace", tags=["marketplace"])

_listings: list[dict[str, Any]] = []
_foods = TraditionalFoodsIndex()
_market = MarketIntelligence()
_cfk = ClimateFinanceKnowledge()


@router.get("/listings")
async def get_listings(
    food: str | None = Query(None),
    county: str | None = Query(None),
    corridor: str | None = Query(None),
    chama: bool | None = Query(None),
):
    results = _listings
    if food:
        results = [l for l in results if food.lower() in l.get("food", "").lower() or food.lower() in l.get("food_sw", "").lower()]
    if county:
        results = [l for l in results if county.lower() == l.get("county", "").lower()]
    if corridor:
        results = [l for l in results if corridor.lower() == l.get("corridor", "").lower()]
    if chama is not None:
        results = [l for l in results if l.get("is_chama") == chama]
    return {"listings": results, "count": len(results)}


@router.post("/listings")
async def create_listing(body: dict):
    food_key = body.get("food", "").lower().replace(" ", "_")
    crop = _foods.classify_crop(food_key)

    listing = {
        "id": str(uuid.uuid4())[:8],
        "seller": body.get("seller", "Anonymous"),
        "food": body.get("food"),
        "food_sw": body.get("food_sw", ""),
        "quantity_kg": body.get("quantity_kg", 0),
        "price_kes_per_kg": body.get("price_kes_per_kg", 0),
        "county": body.get("county", ""),
        "corridor": body.get("corridor", ""),
        "delivery_available": body.get("delivery_available", False),
        "is_chama": body.get("is_chama", False),
        "chama_name": body.get("chama_name", ""),
        "contact": body.get("contact", ""),
        "notes": body.get("notes", ""),
        "status": crop.get("status", "unknown") if crop else "unknown",
        "nutrition": crop.get("nutrition", "") if crop else "",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _listings.append(listing)
    logger.info("listing created: %s — %s (%s)", listing["id"], listing["food"], listing["county"])
    return listing


@router.get("/listings/{listing_id}")
async def get_listing(listing_id: str):
    for l in _listings:
        if l["id"] == listing_id:
            return l
    return {"error": "not found"}


@router.delete("/listings/{listing_id}")
async def delete_listing(listing_id: str):
    global _listings
    _listings = [l for l in _listings if l["id"] != listing_id]
    return {"deleted": True}


@router.get("/listings/{listing_id}/de-risk")
async def listing_de_risk(listing_id: str):
    for l in _listings:
        if l["id"] == listing_id:
            food = l.get("food", "")
            crop = _foods.classify_crop(food)
            rs = crop.get("resilience_score", None) if crop else None
            county = l.get("county", "")
            parametrics = _cfk.get_parametrics(county)
            phl = _cfk.get_phl_analysis(food)
            return {
                "listing_id": listing_id,
                "food": food,
                "resilience_score": rs,
                "parametric_insurance": parametrics,
                "post_harvest_loss": phl,
                "county_risk_context": county,
            }
    return {"error": "not found"}


@router.get("/prices")
async def get_prices():
    prices = {}
    for key, info in _market.MARKET_PRICES.items():
        crop = _foods.classify_crop(key)
        prices[key] = {
            **info,
            "status": crop.get("status", "unknown") if crop else "unknown",
            "name_en": crop.get("name_en", key.replace("_", " ").title()) if crop else key.replace("_", " ").title(),
            "name_sw": crop.get("name_sw", "") if crop else "",
        }
    return {"prices": prices, "count": len(prices)}
