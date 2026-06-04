# Food Roots KE (FRK) — OpenCode Agent Guide

## Project Overview
Traditional Food Intelligence System for Kenya — classifies foods eaten in Nairobi by origin (indigenous vs exotic), maps them to counties and intercropping patterns, and provides climate, market, and de-risking data (parametric insurance, green bond, USAID freeze, post-harvest loss, carbon credits). Of ~680 foods eaten by Nairobians, only about a third are actually from Kenya — the rest are exotic. FRK makes the indigenous ones visible and investable.
Track 4 — Data and Decision Support. Lake Region is the narrative anchor.

## Deploy URLs
- **Frontend**: Netlify drag-and-drop of `frontend/` folder — proxy to Render via `netlify.toml`
- **Backend**: Render via `render.yaml` at food-roots-ke.onrender.com

## Stack
- Python 3.12 + FastAPI 0.136.3
- SQLite (default, file-backed, WAL mode) / Neo4j 5.26.0 optional
- NASA POWER API (satellite, no auth, 179K req/day)
- Open-Meteo (free weather forecast, 10K calls/day, ERA5 from 1940)
- Google Solar API (solar potential)
- Masumi x402 + Cardano escrow (agentic economic autonomy)
- Featherless AI (optional LLM augmentation)
- Neo4j graph database with Cypher query engine
- pytest (150 tests, all passing, zero deprecation warnings)

## Key Rules
1. Always run full test suite after changes: `cd "path\to\frk"; if ($?) { python -m pytest tests/ -v -W error::DeprecationWarning }`
2. Keep all Pydantic V2 patterns (model_config, no deprecated Config class)
3. Use `from __future__ import annotations` in all new Python files
4. Never break the 150-test suite
5. Traditional foods focus — no farmer/loan/credit/securitisation features
6. NASA POWER API is free, no auth — use `satellite.power_client.PowerClient`
7. Frontend is a full SPA (5 pages: Dashboard, Traditional Foods, Corridors, Marketplace, De-Risk) — Tailwind CSS CDN + Chart.js + Leaflet
8. Masumi x402 + Featherless are core infrastructure — use when appropriate
9. **37 crops** in TraditionalFoodsIndex — all with resilience_score (Rs 0.0–1.0), traditional_uses, intercropping, market prices, growing requirements, regions, nutrition context
10. **12 intercropping patterns** with row ratios, hydraulic lift mechanism, yield boost data
11. **9 food corridors** including 2 cross-border (Busia-Uganda, Namanga-Tanzania) and Ukambani-Mombasa — all with WICBT/panya routes/food remittance context
12. **Climate finance/de-risking** is core: parametric insurance (3 satellite triggers, 10-day payout), $772M green bond (4 allocations summing to 100%), USAID freeze ($225M contraction, 87%/42% CSA stats), 57% PHL analytics with 2 interventions, carbon credits (2.5-5.0 tCO2/ha, 3 standards)

## Skills (Slash Commands)
- `/test` or `/verify` — Run full test suite, diagnose failures, verify 150 pass
- `/expand-foods` or `/add-crop` — Research and add new crops to TraditionalFoodsIndex (37 total)
- `/develop-neo4j-graph` — Analyze data, design ontology, ingest into Neo4j
- `/deploy` — Deploy frontend to Netlify + backend to Render

## MCP Servers Available
- **nasa-power** (remote) — NASA POWER API for satellite climate data
- **neo4j-cypher** (stdio) — Cypher query execution against Neo4j. Tools: `get_neo4j_schema_and_indexes`, `read_neo4j_cypher`, `write_neo4j_cypher`
- **x402** (stdio) — Masumi x402 escrow lifecycle for agentic micropayments. Tools: `initiate_escrow`, `lock_escrow`, `submit_data_hash`, `complete_escrow`, `refund_escrow`, `get_escrow_status`, `get_wallet_info`

## File Map
- `knowledge/traditional_foods.py` — TraditionalFoodsIndex with 37 crops, resilience_scores, NUTRITION_MINERALS (7 crops), 12 intercropping patterns, 9 food corridors
- `knowledge/climate_finance.py` — ClimateFinanceKnowledge: parametric insurance, $772M green bond, USAID freeze, 57% PHL, carbon credits, 75M KES fiscal context, cross-border trade (77% women)
- `api/routes/traditional_foods.py` — 8 REST endpoints (classify, region, list, intercropping, corridors, nutrition, nutrition minerals, resilience)
- `api/routes/climate_finance.py` — 6 REST endpoints (/de-risk/overview, /parametrics, /green-bond, /usaid-impact, /post-harvest-loss, /carbon-credits)
- `api/routes/marketplace.py` — 6 REST endpoints (listings browse/post/delete, reference prices, listing de-risk, prices)
- `api/routes/rag.py` — RAG query + POLE traversal endpoints
- `api/routes/weather.py` — Weather + Solar routes
- `api/middleware/` — Error handling, security headers, rate limiting, auth, request ID
- `agriculture_intelligence/precision_farming.py` — CROP_BASE_TEMPS + HARVEST_GDD_THRESHOLDS (37 crops) + INDIGENOUS_AGRONOMIC_TRAITS (C4, hydraulic lift, row ratios, 41.8% yield boost)
- `agriculture_intelligence/land_intelligence.py` — CROP_REQUIREMENTS (37 crops), base yields, market prices
- `agriculture_intelligence/market_intelligence.py` — MARKET_PRICES + RETAIL_MARKUPS (5 AIVs, 40-143%) + VALUE_ADDED_PRICING (KES 400/kg precooked) + WOMEN_TRADERS_SHARE_PCT (77%)
- `graphrag/service.py` — KNOWN_CROPS (37 crops, 50+ variant names) + GraphRAG query engine
- `satellite/power_client.py` — NASA POWER (soil moisture, temp, solar, precip)
- `satellite/openmeteo_client.py` — Open-Meteo 7-day forecast + ERA5 reanalysis
- `satellite/google_environment_client.py` — Google Solar API
- `masumi/escrow_lifecycle.py` — Escrow state machine (RefundAuthorized)
- `masumi/x402_client.py` — x402 HTTP micropayment client
- `masumi/mip003_api.py` — MIP-003 input schema definitions
- `featherless/client.py` — Featherless AI client (optional LLM augmentation)
- `database/` — Repository pattern (SQLite/InMemory/Neo4j), schema migrations
- `tests/` — 150 tests (traditional foods + API + climate finance + marketplace + weather + infrastructure)
- `frontend/` — Full SPA: index.html (5 pages, Tailwind CDN + Chart.js + Leaflet), app.js (all rendering with charts, map, modals, dark mode, i18n), i18n.js (EN/SW), netlify.toml (proxy to Render)
- `render.yaml` — Backend deployment config for Render
- `.opencode/` — OpenCode config, MCP servers, Agent Skills
