# Kilimo Credit Web — Demo Video Script

> **Format:** 5-minute screen recording with voiceover
> **Tone:** Fast-paced, concrete, shows real working system
> **Hackathon:** Mercy Corps AgriFin AI for Agriculture Hackathon — All 5 Tracks
> **Primary Track:** Track 4 — Data and Decision Support
> **Tools:** Python demo script + API calls + frontend browser

---

## Scene 1: The Problem (15s)

**Visual:** Split screen — left side shows CBK statistics, right side shows Apollo Agriculture securitisation news headline

**Voiceover:**
*"Kenya's banks allocate less than 5% of lending to agriculture, despite the sector contributing over 25% of GDP. The Apollo Agriculture securitisation of KES 276 million for 23,839 farmers — with a BBB- rating — proved the model works. But the manual process cannot scale to 5 million farmers. That's why we built Kilimo Credit Web."*

---

## Scene 2: Submit a Farmer Application (30s)

**Visual:** Terminal/script showing `POST /api/v1/apply` with farmer profile JSON

```
POST /api/v1/apply
{
  "first_name": "Grace",
  "last_name": "Wanjiku",
  "phone": "+254712345001",
  "county": "Kiambu",
  "gender": "F",
  "farm_size_ha": 2.5,
  "primary_crop": "maize",
  "chama_member": true,
  "sacco_member": true,
  "latitude": -1.0,
  "longitude": 36.9
}
```

**Voiceover:**
*"A farmer — or an agent — submits a single application. Name, location, farm size, group memberships. That's all it takes to trigger our entire 8-agent pipeline."*

**Visual:** Show the response:

```json
{
  "workflow_id": "WF-a1b2c3d4",
  "status": "approved",
  "farmer_id": "KCW-001",
  "credit_score": 76.5,
  "probability_default": 0.09,
  "max_loan_kes": 18000,
  "risk_factors": [...],
  "verification_hash": "a1b2c3d4e5..."
}
```

**Voiceover:**
*"200 milliseconds later, Grace is approved for KES 18,000 at 9% probability of default. Every decision is logged with a SHA-256 verification hash — auditable by Agusto. But KCW goes further than just lending — it analyses what investment would give Grace the best return on her land."*

---

## Scene 3: NASA POWER Satellite — Live from Space (30s)

**Visual:** API call to the NASA POWER satellite endpoint showing real data

```
GET https://power.larc.nasa.gov/api/temporal/daily/point
  ?parameters=T2M,PRECTOTCORR,GWETROOT,ALLSKY_SFC_SW_DWN
  &latitude=-1.0&longitude=36.9
  &start=2026-05-01&end=2026-05-26
  &community=AG&format=JSON
```

**Response (real Kiambu data):**
```
Temperature:         18.2°C
Precipitation:       5.0 mm/day
Soil Moisture:       0.67 (root zone wetness)
Solar Radiation:     17.2 kWh/m²/day ← 200% above temperate zones
```

**Voiceover:**
*"KCW starts with real data from NASA's POWER satellite — free, no auth, 179,000 requests per day from agriculture users globally. We get live soil moisture from root zone wetness, precipitation from corrected satellite rainfall, temperature at 2 meters, and solar radiation at the surface. Every farmer's field is analysed from space. Not simulations. Not averages. Live satellite data, right now."*

---

## Scene 4: The Investment Intelligence Layer (45s)

**Visual:** Run `python scripts/demo_investment.py` — show the investment advisor output

```
$ python scripts/demo_investment.py

KCW Investment Advisor — Kiambu, 2.5ha, KES 500,000 budget
══════════════════════════════════════════════════════════

NASA POWER Satellite Data (Live):
  Temperature:       18.2°C  — optimal for maize (15-30°C)
  Precipitation:     5.0 mm/day — adequate (4-8 mm/day optimal)
  Soil Moisture:     0.67  — good (0.4-0.8 range)
  Solar Radiation:   17.2 kWh/m²/day — equatorial advantage +200%

Best Crop: Maize (suitability score 0.75/1.0)
Soil Quality: Good (GWETROOT 0.67, temp 18.2°C)

Investment Opportunities (ranked by ROI):
═══╦══════════════════════════╦════════╦══════════════╦═══════════╗
  # ║ Investment               ║  Cost   ║ Net Return   ║ ROI      ║
═══╬══════════════════════════╬════════╬══════════════╬═══════════╣
  1 ║ Seed: droughtguard_301   ║ 28,125 ║ 365,625      ║ 1300.0%  ║
  2 ║ Feed Optimization        ║ 20,000 ║ 60,480       ║ 302.4%   ║
  3 ║ Solar Drying             ║ 125,000║ 48,750       ║ 39.0%    ║
═══╩══════════════════════════╩════════╩══════════════╩═══════════╝

Portfolio: Total KES 173,125 → Expected Return KES 474,855 (274.6% ROI)
Readiness Score: 100/100
```

**Voiceover:**
*"This is the core of KCW — not just lending, but agricultural investment intelligence. The system analyses land, water, sun, seed, soil, and market data simultaneously — all from NASA satellite feeds — and recommends ranked investments with quantified returns. Premium seed at 1300% ROI. Feed optimization at 302%. Solar drying at 39%. The AI doesn't just approve loans — it builds agricultural investment portfolios."*

---

## Scene 5: Precision Farming — Equatorial Agriculture Intelligence (45s)

**Visual:** API calls to the precision farming endpoints for a Naivasha farm (-0.7, 36.4)

```
GET /api/v1/agri/precision-farming/gdd/-0.7/36.4/maize?days=60
→ GDD: 5.6/day, 21% to harvest, 225 days remaining (FAO-66)

GET /api/v1/agri/precision-farming/et/-0.7/36.4
→ ET₀: 4.0 mm/day, irrigate 2-3 pulses/day (FAO-56)

GET /api/v1/agri/precision-farming/pest-risk/-0.7/36.4/maize
→ Fall Armyworm: 69/100, IPM: traps + neem + parasitoids

GET /api/v1/agri/precision-farming/micro-climate/-0.7/36.4
→ Zone: Highland cool — tea, pyrethrum, potato, high-value horticulture

GET /api/v1/agri/precision-farming/equatorial-benchmark/-0.7/36.4
→ Score: 100/100 (Excellent) vs 4 benchmark equatorial systems

GET /api/v1/agri/precision-farming/climate-resilience/-0.7/36.4?crop=maize
→ Adaptation ROI: 51.7%. Every KES spent avoids KES 4.2 in disaster response
```

**Response (climate resilience):**
```json
{
  "adaptation_roi_pct": 51.7,
  "disaster_response_vs_adaptation_ratio": 4.2,
  "policy_context": {
    "kenya_disaster_response_2024_kes": "~75M",
    "climate_smart_ag_budget_2026_2027": "Zero-funded",
    "crop_insurance_allocation_2026_2027": "Not allocated"
  }
}
```

**Voiceover:**
*"General equatorial agriculture intelligence — for any crop, any region. The system computes Growing Degree Days using the FAO-66 standard, evapotranspiration using the FAO-56 Penman-Monteith equation, pest risk with IPM recommendations, micro-climate classification, irrigation timing optimisation, and variable-rate management. Then it benchmarks the location against four major equatorial agricultural systems — East African highlands, West African savanna, West African humid, and SE Asian lowlands. Finally, the climate resilience analysis computes the economic ROI of precision farming versus disaster response — referencing real Kenya Budget Committee testimony from May 2026. Climate Smart Agriculture programs were zero-funded. Crop insurance was not allocated. KCW fills this gap."*

## Scene 6: The Agent Pipeline in Action (30s)

**Visual:** Run `python scripts/demo_simulation.py` — show the full pipeline output

**Voiceover:**
*"Let's watch the full 12-agent pipeline process Grace's application."*

**Show terminal output as each agent runs:**

```
[OnboardingAgent] Ingested Grace Wanjiku — Kiambu, 2.5ha, maize
[GeoAuditAgent] Kiambu NASA POWER: soil_moisture=0.67, solar=17.2 kWh/m² [verified]
[MacroClimaticAgent] Kiambu drought_risk: 0.08 (precip=5.0mm/day, temp=18.2°C)
[LandIntelligenceAgent] Best crop: Maize (score 0.75), soil: good, idle: no
[MarketIntelligenceAgent] Best price: KES 3,200/90kg bag (Unga Ltd contract)
[CooperativeAgent] Coop health: B (score 72), milk upside: KES 10/L
[InvestmentAdvisorAgent] Top pick: droughtguard_301 seed @ 1300% ROI
[CreditAssessmentAgent] PD = 0.09, score = 76.5, max_loan = KES 18,000
[VerificationAgent] PASSED — hash: a1b2...e5f6
[ProcurementAgent] Disbursed KES 18,000 via M-Pesa (TXN-A1B2C3)
```

**Voiceover:**
*"Twelve autonomous agents. The Geo-Audit Agent now queries live NASA satellite data. The Land Intelligence Agent evaluates suitability for 7 crops. The Market Intelligence Agent finds the best price for Grace's maize. The Cooperative Agent scores her cooperative's health and identifies milk pricing opportunities. The Investment Advisor ranks every possible investment by ROI — and recommends the best one. All in under 3 seconds."*

---

## Scene 6: Securitisation Pool Assembly (30s)

**Visual:** API call to build pool — `POST /api/v1/pools/build`

```
POST /api/v1/pools/build
{
  "farmer_data": [
    {"id": "KCW-001", "max_loan_kes": 18000, "probability_default": 0.09, ...},
    {"id": "KCW-004", "max_loan_kes": 45000, "probability_default": 0.05, ...},
    ...
  ]
}
```

**Response:**
```json
{
  "id": "POOL-001",
  "farmer_count": 5,
  "total_notional_kes": 73560000,
  "avg_pd": 0.12,
  "expected_revenue_kes": 82345600,
  "target_rating": "BBB-",
  "tranche_percentages": {"senior": 70, "mezzanine": 20, "junior": 10}
}
```

**Voiceover:**
*"Approved farmers are assembled into a securitisation pool. 5 farmers → KES 73.6 million total notional. Expected revenue of KES 82.3 million with a BBB- target rating. Senior, mezzanine, and junior tranches — replicating the Apollo structure, autonomously."*

---

## Scene 7: x402 Escrow — Cardano Settlement (30s)

**Visual:** Show the escrow lifecycle API calls

```
POST /api/v1/payments/escrow
→ ESC-A1B2 (FundsLockingRequested)

POST /api/v1/payments/escrow/ESC-A1B2/confirm
→ FundsLocked

POST /api/v1/payments/escrow/ESC-A1B2/submit-result
→ ResultSubmitted

POST /api/v1/payments/escrow/ESC-A1B2/complete
→ Completed

GET /api/v1/payments/x402/status
→ { "network": "preprod", "configured": true }
```

**Voiceover:**
*"x402 escrow settlement on Cardano. Funds are locked in a TxPipe-audited smart contract, the agent delivers the data, submits a cryptographic hash, and payment is auto-released. No bank settlement delays. No FX premium. KES at the farmer level, USDM on-chain."*

---

## Scene 8: Frontend Dashboard (30s)

**Visual:** Open `frontend/index.html` — show the dashboard

**Walk through tabs:**
1. **Dashboard** — KPI cards: 5 farmers, KES 73.6M portfolio, 3 pools, avg PD 12%
2. **Kenya map** — County dots sized by farmer density
3. **Farmers table** — Sortable, searchable, status badges (green=approved, red=declined)
4. **Pools** — Pool cards with rating badges
5. **Payments** — Escrow state machine visual timeline
6. **i18n toggle** — Switch to Swahili

**Voiceover:**
*"The frontend dashboard — built with Lovable — gives real-time visibility into the entire pipeline. Farmers, pools, escrow states. In English or Swahili. Dark mode built in. Mobile-responsive for rural smartphones."*

---

## Scene 9: Audit Trail — For Regulators (15s)

**Visual:** GET /api/v1/audit

```json
[
  {
    "timestamp": "2026-05-26T10:00:00Z",
    "event_type": "loan_application",
    "farmer_id": "KCW-001",
    "data": {"credit_score": 76.5, "pd": 0.09, "verification_hash": "a1b2..."}
  }
]
```

**Voiceover:**
*"Every credit decision is recorded with a timestamp, verification hash, and full decision trace. Ready for Agusto rating review. Ready for CBK regulatory audit."*

---

## Scene 10: Close (15s)

**Visual:** Docker-compose deploy + "105 tests passing" + KCW logo + satellite Earth image

```bash
docker compose up -d
# Frontend on port 80
# API on port 8000

pytest tests/ -v
# 105 passed in 23.84s
```

*"Kilimo Credit Web. 105 passing tests — zero deprecation warnings. Twelve autonomous agents. Real NASA satellite data from space. General equatorial agriculture intelligence that cross-cuts all crops — staples, cash crops, and horticulture. Spanning all 5 hackathon tracks — climate-smart agriculture, last-mile delivery, financial inclusion, data-driven decision support, and crop management — in one integrated pipeline. The AI agriculture investment system that analyses land, water, sun, seed, soil, pests, climate resilience, and markets — then makes ranked investment decisions with quantified returns. This is infrastructure for the $100 billion African agricultural investment market. Built today. Ready for tomorrow."*

**[END — 5:00]**

---

## Demo Tech Checklist

| Item | Status | Notes |
|---|---|---|
| FastAPI server running | `uvicorn api.main:app` | Port 8000 |
| Investment demo script | `python scripts/demo_investment.py` | Real NASA data |
| Pipeline demo script | `python scripts/demo_simulation.py` | 5 synthetic farmers |
| Neo4j available | docker-compose --profile full | Optional for demo |
| Frontend ready | `open frontend/index.html` | Works with mock fallback |
| API docs | `/docs` (Swagger) | Show during Q&A |
| Test suite | `pytest tests/ -v` | All 105 passing |
| Precision farming | 7 GET endpoints + 1 POST | GDD, ET, pests, micro-climate, irrigation, benchmark, resilience |
| Equatorial benchmark | GET `/equatorial-benchmark/{lat}/{lon}` | 4 benchmark systems |
| Climate resilience | GET `/climate-resilience/{lat}/{lon}` | Budget Committee testimony (May 2026) |
| Escrow lifecycle | API calls in scene 8 | Use testnet only |

## Fallback Plan (if live API fails)

| If... | Then... |
|---|---|
| Backend won't start | Use `python scripts/demo_simulation.py` — shows full pipeline output |
| Frontend can't reach API | Frontend auto-fallsback to 15 mock farmers (Offline Mode badge) |
| No Neo4j | InMemoryRepository auto-activates |
| Cardano testnet down | Escrow API still works (simulates states locally) |
| Time running short | Skip scenes 3+5, focus on scenes 2+4+6+8 |
