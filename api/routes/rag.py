from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from api.dependencies import get_repository, get_featherless
from database.repository import Repository
from graphrag.service import GraphRAGService

router = APIRouter(prefix="/api/v1/rag", tags=["GraphRAG"])


def get_graphrag(
    repo: Repository = Depends(get_repository),
    featherless: Any = Depends(get_featherless),
) -> GraphRAGService:
    return GraphRAGService(repository=repo, featherless=featherless)


@router.post("/query")
async def rag_query(
    question: str = Query(..., description="Natural language agricultural question"),
    status: Optional[str] = Query(None, description="Filter by farmer status"),
    graphrag: GraphRAGService = Depends(get_graphrag),
):
    filters: dict[str, Any] = {}
    if status:
        filters["status"] = status
    return await graphrag.query(question, **filters)


@router.get("/pole/{farmer_id}")
async def pole_trace(
    farmer_id: str,
    graphrag: GraphRAGService = Depends(get_graphrag),
):
    """POLE+O trace: Person, Location, Event, Organisation for a farmer."""
    result = await graphrag.pole_trace(farmer_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/traverse/{farmer_id}")
async def multi_hop_traverse(
    farmer_id: str,
    hops: int = Query(2, ge=1, le=3, description="Number of hops"),
    graphrag: GraphRAGService = Depends(get_graphrag),
):
    """Multi-hop graph traversal from a farmer node."""
    return await graphrag.multi_hop_traverse(farmer_id, hops=hops)
