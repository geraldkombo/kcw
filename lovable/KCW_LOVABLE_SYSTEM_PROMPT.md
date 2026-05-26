# Kilimo Credit Web — Lovable System Prompt
Copy this prompt to Lovable when uploading the `kcw.zip` archive.

---

You are creating a production-grade dashboard for **Kilimo Credit Web (KCW)**, a decentralised AI-agent platform for smallholder agricultural securitisation in Kenya. This is a real deployable system — 105 passing tests, 40+ API endpoints, 8 autonomous AI agents, real NASA POWER satellite data, and a full precision farming engine.

## Architecture

**Lovable hosts the frontend** (this dashboard). **Backend API runs separately on Render/Fly.io** (free tier). All API calls go to `API_BASE` which defaults to `http://localhost:8000` for local dev but must be configurable via a single `const API_BASE =` at the top of `app.js` so it can be swapped to `https://kcw-api.onrender.com` in production.

```
Frontend (Lovable) ── API calls ──> Backend API (Render)
  /api/v1/farmers                    FastAPI + SQLite
  /api/v1/loans                      NASA POWER satellite data
  /api/v1/apply                      105 tests
  /api/v1/agri/precision-farming/*
```

## Backend API Endpoints

All endpoints live under `API_BASE`:

### System
- `GET /health` — liveness probe `{"status":"ok"}`
- `GET /ready` — readiness probe with DB status
- `GET /api/v1/config` — runtime config

### Farmers
- `GET /api/v1/farmers` — list farmers (query: county, status)
- `POST /api/v1/farmers` — create farmer
- `GET /api/v1/farmers/{id}` — get farmer
- `PATCH /api/v1/farmers/{id}` — update farmer

### Loans
- `GET /api/v1/loans` — list loans (query: farmer_id, status)
- `POST /api/v1/loans` — create loan
- `GET /api/v1/loans/{loan_id}` — get loan
- `PATCH /api/v1/loans/{loan_id}/status` — update loan status

### Apply (multi-agent pipeline)
- `POST /api/v1/apply` — full application. Accepts `{first_name, last_name, phone, gender, county, sub_county, farm_size_ha, primary_crop, chama_member, sacco_member, latitude, longitude, year_registered}`. Returns `{workflow_id, status, farmer_id, assessment: {probability_default, credit_score, approved, max_loan_kes, risk_factors}, settlement, elapsed_seconds}`.

### Securitisation Pools
- `POST /api/v1/pools/build` — `{farmer_data: [{id, max_loan_kes, probability_default, interest_rate_annual, loan_id}]}` → `{id, farmer_count, total_notional_kes, ...}`
- `GET /api/v1/pools` — list pools
- `GET /api/v1/pools/{pool_id}` — get pool

### x402 Payments
- `POST /api/v1/payments/escrow` — create escrow
- `GET /api/v1/payments/escrow/{id}` — get escrow state
- `POST /api/v1/payments/escrow/{id}/confirm` — confirm
- `POST /api/v1/payments/escrow/{id}/submit-result` — submit result
- `POST /api/v1/payments/escrow/{id}/complete` — complete
- `POST /api/v1/payments/escrow/{id}/refund` — refund
- `GET /api/v1/payments/x402/status` — x402 network status

### Audit
- `GET /api/v1/audit` — all audit entries
- `GET /api/v1/audit/{farmer_id}` — audit by farmer

### Agriculture Intelligence (7 subsystems)
- `GET /api/v1/agri/land-suitability?lat=&lon=&crop=` — land suitability
- `GET /api/v1/agri/water/{lat}/{lon}` — water availability
- `GET /api/v1/agri/solar/{lat}/{lon}` — solar potential
- `GET /api/v1/agri/seed/recommend` — seed recommendations
- `GET /api/v1/agri/market-intelligence` — market data
- `GET /api/v1/agri/prices/{crop}` — crop prices
- `GET /api/v1/agri/invest` — investment recommendations
- `GET /api/v1/agri/cooperative/assess` — cooperative health
- `GET /api/v1/agri/contract-farming/search` — contract farming

### Precision Farming (9 subsystems)
- `GET /api/v1/agri/precision-farming/gdd/{lat}/{lon}/{crop}` — growing degree days with equatorial benchmark
- `GET /api/v1/agri/precision-farming/et/{lat}/{lon}` — FAO-56 reference evapotranspiration with benchmark
- `GET /api/v1/agri/precision-farming/pest-risk/{lat}/{lon}/{crop}` — pest/disease risk with IPM, EU export compliance
- `GET /api/v1/agri/precision-farming/micro-climate/{lat}/{lon}` — micro-climate zone classification (5 zones)
- `GET /api/v1/agri/precision-farming/frost-risk/{lat}/{lon}` — frost risk assessment with protective measures
- `GET /api/v1/agri/precision-farming/irrigation-timing/{lat}/{lon}` — optimal irrigation timing
- `GET /api/v1/agri/precision-farming/equatorial-benchmark/{lat}/{lon}` — equatorial suitability index
- `GET /api/v1/agri/precision-farming/climate-resilience/{lat}/{lon}` — climate resilience ROI with policy context (Kenya Budget Committee testimony, May 2026)
- `POST /api/v1/agri/precision-farming` — precision farming full assessment

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend (you) | Vanilla HTML+CSS+JS + Tailwind CSS CDN + Chart.js CDN |
| Backend | Python 3.12 + FastAPI |
| Database | SQLite (WAL mode) by default, Neo4j optional |
| Satellite Data | NASA POWER API (free, no auth) |
| Risk Model | Logistic regression (11 features, gender-disaggregated) |
| Payments | Masumi x402 (Cardano, MIP-003 escrow) |
| Config | Pydantic Settings v2 |

## Key Context for the Dashboard
- **105 tests passing** — this is production-hardened code, not a demo
- **Real satellite data** — NASA POWER daily: temperature, soil moisture, precipitation, solar radiation
- **Kenya Budget 2026-2027**: Climate Smart Agriculture programs zero-funded, crop insurance not allocated, ~75M KES moved to disaster response in 2024 — this is the policy crisis KCW solves
- **Precision farming**: GDD, FAO-56 ET, 8 pest models with IPM, 5 micro-climate zones, frost risk, irrigation timing, equatorial benchmarking, climate resilience ROI (116.7% demonstrated)
- **No LLM needed**: All calculations are deterministic from satellite + market data

## Pages Required

1. **Dashboard** `/` — KPI cards (farmers, active loans, portfolio volume KES, pools), Kenya county SVG map (circle size = farmer density), loan portfolio pie chart, recent activity feed, offline mode badge

2. **Farmers** `/farmers` — searchable table (ID, Name, County, Crop, Credit Score, PD%, Status with colour badges), filter by county/status, detail drawer on row click showing audit trail + risk factor breakdown, pagination

3. **Assess** `/assess` — credit assessment form (first_name, last_name, phone, gender, county, crop, farm_size_ha, chama/sacco checkboxes, lat/lon), submit → loading spinner → result card (approved/declined, credit score, PD, max loan, risk factor list), error handling

4. **Pools** `/pools` — list securitisation pools as cards (farmer count, total notional KES, avg PD%, expected revenue KES, rating badge), button to build new pool from approved farmers

5. **Payments** `/payments` — x402 escrow lifecycle visual timeline, create escrow form, state machine display with colour-coded states (FundsLockingRequested → FundsLocked → ResultSubmitted → Completed / RefundAuthorized → Refunded)

6. **Precision Farming** `/precision-farming` — input lat/lon + crop → fetch and display:
   - GDD score with equatorial benchmark comparison
   - Pest/disease risk (8 models) with IPM recommendations and EU export compliance status
   - Micro-climate zone classification
   - Frost risk level with protective measures
   - Optimal irrigation timing
   - Climate resilience ROI card (adaptation savings, disaster response cost ratio, policy context from Budget Committee testimony)

## Design System
- **Colours**: Primary green `#2E7D32`, accent gold `#FFB300`, earth brown `#5D4037`
- **Dark mode**: Full support, CSS class toggle, persisted in localStorage, respect `prefers-color-scheme`
- **Responsive**: Mobile-first (rural smartphones 320px+), tablet, desktop sidebar layout
- **Typography**: System font stack, 14px base, accessible contrast ratios
- **Accessibility**: ARIA labels, focus outlines, skip-to-content link, semantic HTML, 44px min touch targets
- **Icons**: Emoji only (no icon library dependency)
- **No build step**: Pure CDN-loaded Tailwind CSS and Chart.js

## Technical Requirements
- `API_BASE` variable at top of `app.js` — default `http://localhost:8000`, swap to `https://kcw-api.onrender.com` for production
- All API calls use relative paths from `API_BASE` (no hardcoded localhost in fetch URLs)
- Fail gracefully to mock data when API unreachable — show "Offline Mode" badge in header
- i18n: English + Swahili toggle, store in localStorage, 60+ translation keys
- Toast notification system for success/error/info
- <200KB total JS/CSS, lazy-load Chart.js only when needed
- All numbers formatted: KES with comma separators, percentages to 1 decimal

## Data Models

```json
Farmer: { id, first_name, last_name, phone, county, gender, farm_size_ha, primary_crop, chama_member, sacco_member, credit_score, probability_default, status, created_at }
Loan: { loan_id, farmer_id, amount_kes, interest_rate_annual, purpose, term_months, status, pd_at_origination }
Pool: { pool_id, farmer_count, total_notional_kes, avg_pd, expected_revenue_kes, target_rating, farmers }
Escrow: { escrow_id, state, amount_lovelace, description, history: [{state, timestamp}] }
RiskFactor: { name, value, weight, contribution, direction }
PrecisionFarmingResult: { gdd, et0, pest_risks: [{pest, risk_score, risk_level, ipm_recommendation}], micro_climate_zone, frost_risk, irrigation_timing, climate_resilience: {adaptation_roi_pct, disaster_response_vs_adaptation_ratio, net_savings} }
```

## Mock Data (15 farmers for offline mode)

- Grace Wanjiku, Kiambu, maize, 68.5 score, 12% PD
- Peter Kiprop, Nakuru, maize, 45.0 score, 33% PD
- Achieng Odhiambo, Kisumu, kale, 72.0 score, 8% PD
- Mwangi Kimani, Meru, coffee, 81.0 score, 5% PD
- Mary Mutua, Machakos, beans, 55.0 score, 22% PD
- Jane Chebet, Uasin Gishu, maize, 76.5 score, 9% PD
- Benard Ochieng, Homa Bay, banana, 38.0 score, 42% PD
- Sarah Wekesa, Bungoma, sugarcane, 61.0 score, 17% PD
- Joseph Nyaga, Meru, avocado, 42.0 score, 38% PD
- Faith Njeri, Nyeri, tea, 85.0 score, 3% PD
- David Kiplagat, Nakuru, dairy, 73.0 score, 10% PD
- Agnes Mwikali, Kilifi, tomato, 33.0 score, 48% PD
- Samuel Kipruto, Uasin Gishu, maize, 90.0 score, 2% PD
- Beatrice Akinyi, Kisumu, kale, 48.0 score, 28% PD
- Patrick Muchiri, Kiambu, avocado, 65.0 score, 14% PD

## Kenya County Coordinates (for SVG map)

```json
{"Kiambu": {"x":38,"y":52}, "Nakuru": {"x":33,"y":38}, "Kisumu": {"x":18,"y":45}, "Meru": {"x":60,"y":25}, "Machakos": {"x":52,"y":55}, "Uasin Gishu": {"x":30,"y":28}, "Homa Bay": {"x":20,"y":52}, "Bungoma": {"x":22,"y":22}, "Nyeri": {"x":40,"y":40}, "Kilifi": {"x":70,"y":68}}
```

## Deployment Note

Lovable hosts the frontend. The backend API runs on Render (free tier). Set `API_BASE` in `app.js` to your Render URL before deploying. The existing `frontend/` directory contains a working dashboard — Lovable should rewrite it entirely with the production dashboard described above.
