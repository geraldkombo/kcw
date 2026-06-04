from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Query

from knowledge.traditional_foods import TraditionalFoodsIndex

router = APIRouter(prefix="/api/v1/traditional-foods", tags=["Traditional Foods"])

_tfi = TraditionalFoodsIndex()


@router.get("/classify/{crop}")
async def classify_crop(crop: str):
    """Classify a crop as indigenous, naturalised, or exotic."""
    result = _tfi.classify_crop(crop)
    if not result:
        return {"crop": crop, "classified": False, "note": "Crop not found in traditional foods database"}
    return {
        "crop": crop,
        "classified": True,
        "status": result.get("status"),
        "resilience_score": result.get("resilience_score"),
        "name_sw": result.get("name_sw"),
        "name_en": result.get("name_en"),
        "origin": result.get("origin"),
        "traditional_uses": result.get("traditional_uses"),
        "nutrition": result.get("nutrition"),
        "growing_regions": result.get("regions"),
        "intercropping": result.get("intercropping"),
        "market_demand": result.get("market_demand"),
        "market_price_kes_tonne": result.get("market_price_kes_tonne"),
    }


@router.get("/region/{county}")
async def crops_by_region(county: str):
    """List traditional food plants for a county."""
    crops = _tfi.get_crops_for_region(county)
    if not crops:
        return {"county": county, "crop_count": 0, "crops": [], "note": "No traditional foods data for this county"}
    return {
        "county": county,
        "crop_count": len(crops),
        "crops": [
            {
                "name_sw": c.get("name_sw", "").split("/")[0].strip(),
                "name_en": c.get("name_en", ""),
                "status": c.get("status", ""),
                "resilience_score": c.get("resilience_score"),
                "origin": c.get("origin", ""),
                "nutrition": c.get("nutrition", ""),
                "traditional_uses": c.get("traditional_uses", ""),
                "growing_days": c.get("growing_days"),
                "market_price_kes_tonne": c.get("market_price_kes_tonne"),
                "market_demand": c.get("market_demand"),
            }
            for c in crops
        ],
    }


@router.get("/intercropping")
async def intercropping_patterns(county: Optional[str] = Query(None, description="Filter by county")):
    """Get traditional intercropping patterns."""
    patterns = _tfi.get_intercropping_patterns(county)
    return {
        "count": len(patterns),
        "patterns": patterns,
        "source": "Traditional food knowledge — Kenya AI Challenge workshop (2026)",
    }

@router.get("/corridors")
async def food_corridors(county: Optional[str] = Query(None, description="Filter by origin county")):
    """Get ethnic food demand corridors connecting counties to Nairobi."""
    corridors = _tfi.get_food_corridors(county)
    return {
        "count": len(corridors),
        "corridors": corridors,
        "source": "Traditional food knowledge — Kenya AI Challenge workshop (2026)",
    }


@router.get("/resilience")
async def resilience_rating(
    crops: str = Query(..., description="Comma-separated list of crops"),
):
    """Rate a set of crops for climate resilience based on indigenous knowledge."""
    crop_list = [c.strip().lower() for c in crops.split(",")]
    rating = _tfi.get_resilience_rating(crop_list)
    return rating


@router.get("/nutrition/{crop}")
async def nutritional_context(crop: str):
    """Get nutritional context for a crop in the traditional food system."""
    ctx = _tfi.get_nutritional_context(crop)
    if not ctx:
        return {"crop": crop, "note": "Crop not found in database"}
    return ctx


@router.get("/nutrition/{crop}/minerals")
async def nutrition_minerals(crop: str):
    """Get detailed mineral composition (Fe, Ca, P, K, Mg, Na) for a crop in mg/kg dry weight."""
    ctx = _tfi.get_nutrition_minerals(crop)
    if not ctx:
        return {"crop": crop, "note": "Crop not found in database"}
    return ctx


@router.get("/list")
async def list_all_crops(status: Optional[str] = Query(None, description="Filter by status: indigenous, naturalised, exotic")):
    """List all traditional food plants, optionally filtered by status."""
    if status:
        crops = _tfi.list_by_status(status)
    else:
        crops = _tfi.list_all()
    return {
        "count": len(crops),
        "status_filter": status or "all",
        "crops": [
            {
                "key": c.get("key"),
                "name_sw": c.get("name_sw", "").split("/")[0].strip(),
                "name_en": c.get("name_en", ""),
                "status": c.get("status", ""),
                "resilience_score": c.get("resilience_score"),
                "origin": c.get("origin", ""),
                "regions": c.get("regions", []),
                "market_price_kes_tonne": c.get("market_price_kes_tonne"),
            }
            for c in crops
        ],
    }
