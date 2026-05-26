# Kilimo Credit Web (KCW) — OpenCode Agent Guide

## Project Overview
AI Agriculture Investment System — autonomous NASA satellite data pipeline to ranked investment recommendations.
Mercy Corps AgriFin AI for Agriculture Hackathon entry. Primary track: Track 4 (Data and Decision Support).
Spans all 5 challenge tracks. Evaluation: User Relevance, Feasibility & Scalability, Inclusivity & Gender.

## Stack
- Python 3.12 + FastAPI 0.136.3
- Neo4j 5.26.0 (Cypher 25 SEARCH)
- NASA POWER API (satellite soil/water/sun data, no auth)
- Masumi x402 + Cardano escrow
- Featherless AI (optional LLM augmentation)
- Lovable MCP (optional frontend generation)
- pytest 9.0.3 (76 tests, all passing)

## Key Rules
1. Always run full test suite after changes: `pytest tests/ -v -W error::DeprecationWarning`
2. Keep all Pydantic V2 patterns (model_config, no deprecated Config class)
3. Use `from __future__ import annotations` in all new Python files
4. Never break the 76-test suite (12 agents, 38+ endpoints, 7 intelligence subsystems)
5. Investment system focus: not just credit scoring, but agricultural investment intelligence
5. Verify proposals against official May 2026 documentation before making claims
6. NASA POWER API is free, no auth — use `satellite/power_client.PowerClient` for real satellite data
7. All 8 agents live in `agents/` — orchestrator coordinates the pipeline

## File Map
- `satellite/power_client.py` — NASA POWER satellite API (soil moisture, temp, solar, precip)
- `sprout/client.py` — Sprout CKAN content API (Mercy Corps AgriFin advisory content)
- `masumi/escrow_lifecycle.py` — Escrow state machine (includes RefundAuthorized)
- `agents/` — 12 AI agents (Orchestrator, Onboarding, Geo-Audit, Macro-Climatic, LandIntelligence, MarketIntelligence, Cooperative, InvestmentAdvisor, Credit, V&V, Procurement, Liquidity)
- `agriculture_intelligence/` — 7 subsystems (LandIntelligence, WaterOptimizer, SolarOptimizer, SeedQualityAnalyzer, MarketIntelligence, CooperativeManager, InvestmentAdvisor)
- `satellite/power_client.py` — NASA POWER real satellite data integration
- `tests/` — 76 tests across 4 suites
- `frontend/index.html` — SPA dashboard (dark mode, EN/SW i18n)
