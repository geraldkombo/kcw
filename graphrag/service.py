from __future__ import annotations

import json
import logging
from typing import Any, Optional

from database.repository import Neo4jRepository, Repository
from knowledge.traditional_foods import TraditionalFoodsIndex

logger = logging.getLogger("frk.graphrag")

# Known counties and crops for keyword-based entity extraction fallback
KNOWN_COUNTIES = [
    "kiambu", "nakuru", "kisumu", "meru", "machakos", "uasin gishu",
    "homa bay", "bungoma", "kilifi", "nyeri", "nairobi", "kajiado",
    "laikipia", "trans nzoia", "elgeyo marakwet", "nandi", "kakamega",
    "busi a", "siaya", "migori", "kisii", "nyamira", "muranga",
    "kirinyaga", "embu", "tharaka nithi", "isiolo", "marsabit",
    "mandera", "wajir", "garissa", "tana river", "lamu", "tai ta taveta",
    "kwale", "mombasa", "vihiga", "baringo", "samburu", "turkana",
    "west pokot",
]

KNOWN_CROPS = [
    "maize", "beans", "coffee", "tea", "kale", "avocado", "banana",
    "dairy", "tomato", "sugarcane", "cassava", "sweet potato",
    "millet", "sorghum", "groundnut", "cowpea", "cabbage", "spinach",
    "onion", "mango", "passion fruit", "papaya", "rice", "wheat",
    "pyrethrum", "cotton", "macadamia", "coconut", "cashew",
    # Indigenous / traditional food plants (Maundu, 1999)
    "amaranth", "terere", "mchicha",
    "black nightshade", "managu", "osusu", "african nightshade",
    "spider plant", "sagaa", "mnavu", "mlenda", "cat's whiskers",
    "cowpea leaves", "kunde", "choroko",
    "jute mallow", "mrenda", "murere", "apoth",
    "pumpkin leaves", "majani ya malenge", "murenda",
    "finger millet", "wimbi", "ugali",
    "pigeon pea", "mbaazi", "njahi", "gongo pea",
    "bambara nut", "njugu mawe", "nyimo",
    "baobab", "mbuyu",
    "tamarind", "ukwaju",
    "yam", "kiasi", "mayuni",
    # Ojwang (2020) — Homa Bay traditional foods
    "dek", "mito", "boo", "atipa", "odielo", "ndemra", "alikra", "osoyi",
    "ng'or", "ng_or",
    "mapera", "ochuoga", "akuno", "sangla", "nyatonglo",
    "slenderleaf", "mitoo", "marejea", "crotalaria",
    "desert date", "desert_date", "mchunju", "balanites",
    "bird plum", "bird_plum", "mkuni", "ekalale",
    "vitex", "black plum", "vitex_black_plum", "mfudu", "jwelu",
]

KNOWN_STATUSES = ["active", "repaid", "defaulted", "delinquent", "completed"]


class GraphRAGService:
    """Graph-powered retrieval-augmented generation for agricultural intelligence.

    Pipeline:
      1. Entity extraction — identify counties, crops, farmer IDs from question
      2. Seed finding — locate matching nodes in the graph (Neo4j or simulated)
      3. Context expansion — multi-hop relationship traversal
      4. LLM synthesis — Featherless generates grounded answer from graph context

    Works with both Neo4j (native Cypher) and SQLite (simulated graph traversal).
    """

    def __init__(self, repository: Repository, featherless: Any = None) -> None:
        self._repo = repository
        self._llm = featherless
        self._is_neo4j = isinstance(repository, Neo4jRepository)
        self._tfi = TraditionalFoodsIndex()

    async def query(
        self,
        question: str,
        **filters: Any,
    ) -> dict[str, Any]:
        entities = await self._extract_entities(question)
        seeds = await self._find_seeds(entities, filters)
        context = await self._expand_context(seeds)

        # Traditional food plants context (Maundu, 1999)
        traditional_foods = {}
        for county in entities.get("counties", []):
            crops = self._tfi.get_crops_for_region(county)
            if crops:
                traditional_foods[county] = {
                    "count": len(crops),
                    "indigenous": [
                        {"name_sw": c.get("name_sw", "").split("/")[0].strip(),
                         "name_en": c.get("name_en", ""),
                         "status": c.get("status"),
                         "market_price_kes_tonne": c.get("market_price_kes_tonne")}
                        for c in crops if c.get("status") == "indigenous"
                    ],
                }
            patterns = self._tfi.get_intercropping_patterns(county)
            if patterns:
                if county not in traditional_foods:
                    traditional_foods[county] = {}
                traditional_foods[county]["intercropping"] = patterns

        # Classify any crops mentioned in the question
        classified_crops = {}
        for crop in entities.get("crops", []):
            info = self._tfi.classify_crop(crop)
            if info:
                classified_crops[crop] = {
                    "status": info.get("status"),
                    "origin": info.get("origin"),
                    "nutrition": info.get("nutrition"),
                    "market_price_kes_tonne": info.get("market_price_kes_tonne"),
                }

        # Resilience rating for detected crops
        resilience = self._tfi.get_resilience_rating(entities.get("crops", []))

        answer = await self._synthesize(question, context, entities, traditional_foods, classified_crops)
        return {
            "question": question,
            "answer": answer,
            "entities_extracted": entities,
            "traditional_foods": {
                "county_crops": traditional_foods,
                "classified_crops": classified_crops,
                "resilience": resilience,
                "source": "Traditional food knowledge (2026)",
            } if traditional_foods or classified_crops else {},
            "seeds_found": [
                {k: v for k, v in s.items() if k != "embedding"}
                for s in seeds[:10]
            ],
            "graph_context": {
                "nodes_visited": len(context),
                "relationships": context[:20],
            },
        }

    async def pole_trace(self, farmer_id: str) -> dict[str, Any]:
        """POLE+O trace: Person, Location, Event, Organisation for a farmer."""
        if self._is_neo4j:
            result = await self._repo.run(
                """
                MATCH (f:FarmingHousehold {farmer_id: $farmer_id})
                OPTIONAL MATCH (f)-[:LOCATED_IN]->(c:County)
                OPTIONAL MATCH (f)-[:GROWS]->(cr:Crop)
                OPTIONAL MATCH (f)-[:MEMBER_OF]->(s:SACCO)
                OPTIONAL MATCH (f)-[:HAS_LOAN]->(l:Loan)
                RETURN f.first_name + ' ' + f.last_name AS person,
                       c.name AS location,
                       cr.name AS event_crop,
                       s.name AS organisation,
                       COUNT(DISTINCT l) AS loan_count,
                       AVG(l.amount_kes) AS avg_loan_kes
                """,
                {"farmer_id": farmer_id},
            )
            return result[0] if result else {"error": "farmer not found"}
        else:
            farmer = self._repo.get_farmer(farmer_id)
            if not farmer:
                return {"error": "farmer not found"}
            data = farmer.get("data", farmer)
            if isinstance(data, str):
                data = json.loads(data)
            return {
                "person": f"{data.get('first_name', '')} {data.get('last_name', '')}",
                "location": data.get("county", "unknown"),
                "event_crop": data.get("primary_crop", "unknown"),
                "organisation": "N/A",
                "loan_count": 0,
                "avg_loan_kes": None,
            }

    async def multi_hop_traverse(
        self,
        farmer_id: str,
        hops: int = 2,
    ) -> list[dict[str, Any]]:
        """Multi-hop graph traversal: Farmer -> County -> Peer Farmers -> Loans."""
        if not self._is_neo4j:
            return [{"warning": "multi-hop traversal requires Neo4j"}]

        if hops >= 1:
            q1 = """
                MATCH (f:FarmingHousehold {farmer_id: $farmer_id})-[:LOCATED_IN]->(c:County)
                RETURN c.name AS county, c.region AS region
            """
            county_info = await self._repo.run(q1, {"farmer_id": farmer_id})
        else:
            county_info = []

        if hops >= 2:
            q2 = """
                MATCH (f:FarmingHousehold {farmer_id: $farmer_id})-[:LOCATED_IN]->(c:County)
                MATCH (c)<-[:LOCATED_IN]-(peer:FarmingHousehold)
                WHERE peer.farmer_id <> $farmer_id
                RETURN peer.farmer_id, peer.first_name, peer.last_name,
                       peer.primary_crop, peer.credit_score, peer.probability_default
                LIMIT 20
            """
            peers = await self._repo.run(q2, {"farmer_id": farmer_id})
        else:
            peers = []

        if hops >= 3:
            q3 = """
                MATCH (f:FarmingHousehold {farmer_id: $farmer_id})-[:LOCATED_IN]->(c:County)
                MATCH (c)<-[:LOCATED_IN]-(peer:FarmingHousehold)
                WHERE peer.farmer_id <> $farmer_id
                MATCH (peer)-[:HAS_LOAN]->(l:Loan)
                RETURN c.name AS county,
                       COUNT(DISTINCT peer) AS peer_count,
                       AVG(l.amount_kes) AS avg_loan_kes,
                       SUM(CASE WHEN l.status = 'defaulted' THEN 1 ELSE 0 END) * 1.0 / COUNT(l) AS default_rate
            """
            loan_agg = await self._repo.run(q3, {"farmer_id": farmer_id})
        else:
            loan_agg = []

        result = []
        if county_info:
            result.append({"hop": 1, "type": "county", "data": county_info[0]})
        if peers:
            result.append({"hop": 2, "type": "peer_farmers", "count": len(peers), "data": peers[:5]})
        if loan_agg:
            result.append({"hop": 3, "type": "loan_aggregation", "data": loan_agg[0]})

        return result

    async def _extract_entities(self, question: str) -> dict[str, Any]:
        q = question.lower()
        counties = [c for c in KNOWN_COUNTIES if c in q]
        crops = [c for c in KNOWN_CROPS if c in q]
        statuses = [s for s in KNOWN_STATUSES if s in q]

        entities: dict[str, Any] = {
            "counties": counties,
            "crops": crops,
            "statuses": statuses,
            "raw": question,
        }

        if self._llm is not None:
            try:
                result = await self._llm.chat_completion(
                    model="google/gemma-4-27b-it",
                    messages=[
                        {
                            "role": "system",
                            "content": "Extract agricultural entities from the question. "
                            "Return JSON with keys: counties (list), crops (list), "
                            "farmer_ids (list), statuses (list), loan_purposes (list). "
                            "Use empty lists for missing entities.",
                        },
                        {"role": "user", "content": question},
                    ],
                    temperature=0.1,
                    max_tokens=512,
                )
                content = result["choices"][0]["message"]["content"]
                try:
                    llm_entities = json.loads(content)
                    entities["counties"] = list(set(
                        entities["counties"] + [c.lower() for c in llm_entities.get("counties", [])]
                    ))
                    entities["crops"] = list(set(
                        entities["crops"] + [c.lower() for c in llm_entities.get("crops", [])]
                    ))
                    entities["farmer_ids"] = llm_entities.get("farmer_ids", [])
                    entities["purposes"] = llm_entities.get("loan_purposes", [])
                except (json.JSONDecodeError, KeyError):
                    logger.warning("LLM entity extraction returned non-JSON: %s", content[:200])
            except Exception:
                logger.exception("LLM entity extraction failed")

        return entities

    async def _find_seeds(
        self,
        entities: dict[str, Any],
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        seeds: list[dict[str, Any]] = []

        if self._is_neo4j:
            for county in entities.get("counties", []):
                rows = await self._repo.run(
                    """
                    MATCH (f:FarmingHousehold)
                    WHERE toLower(f.county) = $county
                    RETURN f.farmer_id AS farmer_id,
                           f.first_name AS first_name,
                           f.last_name AS last_name,
                           f.county AS county,
                           f.primary_crop AS crop,
                           f.credit_score AS credit_score,
                           f.probability_default AS probability_default,
                           f.status AS status
                    LIMIT 20
                    """,
                    {"county": county},
                )
                seeds.extend(rows)

            for crop in entities.get("crops", []):
                rows = await self._repo.run(
                    """
                    MATCH (f:FarmingHousehold)
                    WHERE toLower(f.primary_crop) = $crop
                    RETURN f.farmer_id AS farmer_id,
                           f.first_name AS first_name,
                           f.last_name AS last_name,
                           f.county AS county,
                           f.primary_crop AS crop,
                           f.credit_score AS credit_score,
                           f.probability_default AS probability_default,
                           f.status AS status
                    LIMIT 20
                    """,
                    {"crop": crop},
                )
                seeds.extend(rows)

            for fid in entities.get("farmer_ids", []):
                rows = await self._repo.run(
                    "MATCH (f:FarmingHousehold {farmer_id: $fid}) RETURN f",
                    {"fid": fid},
                )
                seeds.extend(rows)

            status_filter = entities.get("statuses", filters.get("status", []))
            if isinstance(status_filter, str):
                status_filter = [status_filter]
            for status in status_filter:
                rows = await self._repo.run(
                    """
                    MATCH (f:FarmingHousehold)
                    WHERE f.status = $status
                    RETURN f.farmer_id AS farmer_id,
                           f.first_name AS first_name,
                           f.last_name AS last_name,
                           f.county AS county,
                           f.status AS status,
                           f.credit_score AS credit_score
                    LIMIT 20
                    """,
                    {"status": status},
                )
                seeds.extend(rows)
        else:
            farmers = self._repo.list_farmers()
            for farmer in farmers:
                data = farmer.get("data", farmer)
                if isinstance(data, str):
                    data = json.loads(data)
                f_county = (data.get("county") or "").lower()
                f_crop = (data.get("primary_crop") or "").lower()
                f_status = (data.get("status") or "").lower()
                f_id = (data.get("farmer_id") or "").lower()

                matched = False
                if any(c in f_county for c in entities.get("counties", [])):
                    matched = True
                if any(c in f_crop for c in entities.get("crops", [])):
                    matched = True
                if any(fid.lower() == f_id for fid in entities.get("farmer_ids", [])):
                    matched = True
                if any(s == f_status for s in entities.get("statuses", [])):
                    matched = True

                if matched:
                    seeds.append({
                        "farmer_id": data.get("farmer_id"),
                        "first_name": data.get("first_name"),
                        "last_name": data.get("last_name"),
                        "county": data.get("county"),
                        "crop": data.get("primary_crop"),
                        "credit_score": data.get("credit_score"),
                        "status": data.get("status"),
                    })

        return seeds

    async def _expand_context(
        self,
        seeds: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        context: list[dict[str, Any]] = []
        if not seeds:
            return context

        for seed in seeds[:5]:
            fid = seed.get("farmer_id") or seed.get("farmer_id")
            if not fid:
                continue

            pole = await self.pole_trace(fid)
            context.append({
                "seed": {
                    "farmer_id": fid,
                    "person": seed.get("first_name", "") + " " + seed.get("last_name", ""),
                    "county": seed.get("county"),
                    "crop": seed.get("crop"),
                    "credit_score": seed.get("credit_score"),
                    "status": seed.get("status"),
                },
                "pole_trace": pole,
            })

            if self._is_neo4j:
                hops = await self.multi_hop_traverse(fid, hops=2)
                context[-1]["graph_hops"] = hops
            else:
                loans = self._repo.list_loans()
                farmer_loans = [
                    l for l in loans
                    if l.get("farmer_id") == fid
                    or (isinstance(l.get("data"), dict) and l["data"].get("farmer_id") == fid)
                ]
                context[-1]["loans"] = farmer_loans[:5]

        return context

    async def _synthesize(
        self,
        question: str,
        context: list[dict[str, Any]],
        entities: dict[str, Any],
        traditional_foods: dict[str, Any] | None = None,
        classified_crops: dict[str, Any] | None = None,
    ) -> str:
        if not context:
            return ("I couldn't find relevant agricultural data to answer this question. "
                    "Try specifying a county (e.g., Nakuru, Kiambu), crop (e.g., maize, coffee), "
                    "or farmer ID.")

        context_summary = json.dumps(context, indent=2, default=str)[:3000]
        tf_summary = json.dumps({
            "traditional_foods": traditional_foods or {},
            "classified_crops": classified_crops or {},
        }, indent=2, default=str)[:1000]

        if self._llm is not None:
            try:
                result = await self._llm.chat_completion(
                    model="deepseek/deepseek-v4-pro",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an agricultural intelligence analyst for Food Roots KE. "
                            "Answer the farmer's question using ONLY the context provided. "
                            "Reference specific farmers, counties, crops, and data points. "
                            "Be concise and actionable. If the data doesn't answer the question, "
                            "say what data IS available.",
                        },
                        {
                            "role": "user",
                            "content": f"Question: {question}\n\nGraph context:\n{context_summary}\n\nTraditional food plants context (Maundu, 1999):\n{tf_summary}",
                        },
                    ],
                    temperature=0.2,
                    max_tokens=1024,
                )
                return result["choices"][0]["message"]["content"]
            except Exception:
                logger.exception("LLM synthesis failed")

        return self._fallback_synthesis(question, context, entities, classified_crops)

    def _fallback_synthesis(
        self,
        question: str,
        context: list[dict[str, Any]],
        entities: dict[str, Any],
        classified_crops: dict[str, Any] | None = None,
    ) -> str:
        if classified_crops is None:
            classified_crops = {}
        parts: list[str] = []
        counties = entities.get("counties", [])
        crops = entities.get("crops", [])

        if counties:
            parts.append(f"Found data for {', '.join(counties).title()}.")
        if crops:
            parts.append(f"Related crops: {', '.join(crops)}.")

        seed_count = len(context)
        if seed_count > 0:
            scores = [
                c["seed"].get("credit_score")
                for c in context
                if c["seed"].get("credit_score") is not None
            ]
            if scores:
                avg = sum(scores) / len(scores)
                parts.append(f"Average credit score across {seed_count} farmers: {avg:.1f}.")

            high_risk = [
                c["seed"] for c in context
                if c["seed"].get("credit_score") is not None and c["seed"]["credit_score"] < 50
            ]
            if high_risk:
                parts.append(
                    f"High-risk farmers ({len(high_risk)}): "
                    + ", ".join(f"{h['person']} ({h['county']})" for h in high_risk[:3])
                    + "."
                )

            top = sorted(
                [c["seed"] for c in context if c["seed"].get("credit_score") is not None],
                key=lambda x: x["credit_score"],
                reverse=True,
            )[:3]
            if top:
                parts.append(
                    "Top performers: "
                    + ", ".join(f"{t['person']} (score: {t['credit_score']})" for t in top)
                    + "."
                )

            loan_data = [
                c["loans"] for c in context if c.get("loans")
            ]
            if loan_data:
                total_loans = sum(len(ls) for ls in loan_data)
                parts.append(f"{total_loans} loan records found across matched farmers.")

        if classified_crops:
            for crop, info in classified_crops.items():
                status = info.get("status", "unknown")
                origin = info.get("origin", "unknown")
                price = info.get("market_price_kes_tonne")
                parts.append(
                    f"{crop.title()}: {status} ({origin}), "
                    f"{'KES ' + f'{price:,}/t' if price else 'price data unavailable'}."
                )

        return " ".join(parts) if parts else "No agricultural data matched your query."
