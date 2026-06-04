from __future__ import annotations

import pytest

from database.repository import InMemoryRepository
from graphrag.service import GraphRAGService

pytestmark = pytest.mark.anyio


@pytest.fixture
def repo():
    r = InMemoryRepository()
    r.save_farmer({
        "farmer_id": "KCW-001",
        "first_name": "Grace",
        "last_name": "Wanjiku",
        "county": "Kiambu",
        "primary_crop": "maize",
        "credit_score": 68.5,
        "probability_default": 0.12,
        "status": "active",
        "phone": "+254712345001",
        "gender": "F",
        "farm_size_ha": 2.5,
    })
    r.save_farmer({
        "farmer_id": "KCW-002",
        "first_name": "Peter",
        "last_name": "Kiprop",
        "county": "Nakuru",
        "primary_crop": "maize",
        "credit_score": 45.0,
        "probability_default": 0.33,
        "status": "active",
        "phone": "+254712345002",
        "gender": "M",
        "farm_size_ha": 4.0,
    })
    r.save_farmer({
        "farmer_id": "KCW-003",
        "first_name": "Achieng",
        "last_name": "Odhiambo",
        "county": "Kisumu",
        "primary_crop": "kale",
        "credit_score": 72.0,
        "probability_default": 0.08,
        "status": "active",
        "phone": "+254712345003",
        "gender": "F",
        "farm_size_ha": 1.2,
    })
    r.save_farmer({
        "farmer_id": "KCW-004",
        "first_name": "Mwangi",
        "last_name": "Kimani",
        "county": "Meru",
        "primary_crop": "coffee",
        "credit_score": 81.0,
        "probability_default": 0.05,
        "status": "delinquent",
        "phone": "+254712345004",
        "gender": "M",
        "farm_size_ha": 3.0,
    })
    r.save_loan({
        "loan_id": "LN-001",
        "farmer_id": "KCW-001",
        "amount_kes": 18000,
        "status": "repaid",
    })
    r.save_loan({
        "loan_id": "LN-009",
        "farmer_id": "KCW-004",
        "amount_kes": 15000,
        "status": "defaulted",
    })
    return r


@pytest.fixture
def service(repo):
    return GraphRAGService(repository=repo, featherless=None)


class TestGraphRAGEntityExtraction:
    async def test_extracts_county_from_question(self, service):
        entities = await service._extract_entities("What farmers are in Nakuru?")
        assert "nakuru" in entities["counties"]

    async def test_extracts_crop_from_question(self, service):
        entities = await service._extract_entities("Show me maize farmers")
        assert "maize" in entities["crops"]

    async def test_extracts_multiple_entities(self, service):
        entities = await service._extract_entities("Coffee farmers in Meru with delinquent status")
        assert "coffee" in entities["crops"]
        assert "meru" in entities["counties"]
        assert "delinquent" in entities["statuses"]

    async def test_returns_empty_lists_for_no_match(self, service):
        entities = await service._extract_entities("What is the weather today?")
        assert entities["counties"] == []
        assert entities["crops"] == []


class TestGraphRAGSeedFinding:
    async def test_finds_by_county(self, service):
        entities = {"counties": ["nakuru"], "crops": [], "farmer_ids": [], "statuses": []}
        seeds = await service._find_seeds(entities, {})
        assert len(seeds) >= 1
        assert any("Peter" in s.get("first_name", "") for s in seeds)

    async def test_finds_by_crop(self, service):
        entities = {"counties": [], "crops": ["kale"], "farmer_ids": [], "statuses": []}
        seeds = await service._find_seeds(entities, {})
        assert len(seeds) >= 1
        assert any("Achieng" in s.get("first_name", "") for s in seeds)

    async def test_finds_by_status(self, service):
        entities = {"counties": [], "crops": [], "farmer_ids": [], "statuses": ["delinquent"]}
        seeds = await service._find_seeds(entities, {})
        assert len(seeds) >= 1
        assert any(s.get("status") == "delinquent" for s in seeds)

    async def test_finds_by_farmer_id(self, service):
        entities = {"counties": [], "crops": [], "farmer_ids": ["KCW-001"], "statuses": []}
        seeds = await service._find_seeds(entities, {})
        assert len(seeds) >= 1
        assert seeds[0]["farmer_id"] == "KCW-001"


class TestGraphRAGQuery:
    async def test_query_by_county_returns_structured_result(self, service):
        result = await service.query("Farmers in Kiambu")
        assert result["question"] == "Farmers in Kiambu"
        assert "kiambu" in str(result["entities_extracted"]["counties"]).lower()
        assert len(result["seeds_found"]) >= 1
        assert result["answer"]

    async def test_query_by_crop_returns_answer(self, service):
        result = await service.query("Maize farmers")
        assert "maize" in str(result["entities_extracted"]["crops"])
        assert result["answer"]

    async def test_query_no_match_returns_fallback(self, service):
        result = await service.query("Elephant farmers in Timbuktu")
        assert result["answer"]

    async def test_pole_trace_returns_entity(self, service):
        trace = await service.pole_trace("KCW-001")
        assert "error" not in trace
        assert trace["person"]
        assert trace["location"] == "Kiambu"

    async def test_pole_trace_nonexistent_returns_error(self, service):
        trace = await service.pole_trace("KCW-999")
        assert "error" in trace

    async def test_multi_hop_without_neo4j_returns_warning(self, service):
        hops = await service.multi_hop_traverse("KCW-001", hops=2)
        assert len(hops) == 0 or "warning" in hops[0]

    async def test_query_with_status_filter(self, service):
        result = await service.query("Delinquent farmers", status="delinquent")
        seeds = result["seeds_found"]
        if seeds:
            assert any(s.get("status") == "delinquent" for s in seeds)


class TestGraphRAGFallbackSynthesis:
    async def test_fallback_with_credit_scores(self, service):
        entities = {"counties": ["kiambu"], "crops": ["maize"], "farmer_ids": [], "statuses": []}
        context = [
            {
                "seed": {
                    "farmer_id": "KCW-001",
                    "person": "Grace Wanjiku",
                    "county": "Kiambu",
                    "crop": "maize",
                    "credit_score": 68.5,
                    "status": "active",
                },
            },
        ]
        answer = service._fallback_synthesis("Kiambu farmers", context, entities)
        assert "Kiambu" in answer
        assert "68.5" in answer
        assert "Grace" in answer

    async def test_fallback_empty_context(self, service):
        answer = service._fallback_synthesis("test", [], {})
        assert "no agricultural data" in answer.lower()

    async def test_fallback_highlights_high_risk(self, service):
        entities = {"counties": ["nakuru"], "crops": [], "farmer_ids": [], "statuses": []}
        context = [
            {
                "seed": {
                    "farmer_id": "KCW-002",
                    "person": "Peter Kiprop",
                    "county": "Nakuru",
                    "crop": "maize",
                    "credit_score": 45.0,
                    "status": "active",
                },
            },
        ]
        answer = service._fallback_synthesis("Nakuru farmers", context, entities)
        assert "high-risk" in answer.lower() or "Peter" in answer
