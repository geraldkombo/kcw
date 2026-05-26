# Kilimo Credit Web — Demo Outputs (Live API)

Generated from live API at `localhost:8000` on 26 May 2026.
All data sourced from NASA POWER satellite (free, no auth).

## Locations

| Site | Latitude | Longitude | County | Agro-ecology |
|------|----------|-----------|--------|-------------|
| Naivasha | -0.70 | 36.40 | Nakuru | Highland cool (2000-3000m) |
| Kiambu | -1.00 | 36.90 | Kiambu | Highland warm (1500-2500m) |
| Vihiga | +0.05 | 34.70 | Vihiga | Highland warm (1500-2500m) |

---

## 1. Growing Degree Days (FAO-66)

### Naivasha (-0.7, 36.4) — 15.6°C mean
| Crop | GDD/day | GDD/60d | % to harvest | Days to harvest |
|------|---------|---------|-------------|----------------|
| Maize (base 10°C) | 5.6 | 336.6 | 21.0% | 225 |
| Rose (base 7°C) | 8.6 | 516.6 | 20.7% | 230 |

### Kiambu (-1.0, 36.9) — 18.2°C mean
| Crop | GDD/day | GDD/60d | % to harvest | Days to harvest |
|------|---------|---------|-------------|----------------|
| Maize (base 10°C) | 8.2 | 490.8 | 30.7% | 136 |
| Rose (base 7°C) | 11.2 | 670.8 | 26.8% | 164 |

### Vihiga (0.05, 34.7) — 19.7°C mean
| Crop | GDD/day | GDD/60d | % to harvest | Days to harvest |
|------|---------|---------|-------------|----------------|
| Maize (base 10°C) | 9.7 | 581.4 | 36.3% | 105 |
| Rose (base 7°C) | 12.7 | 761.4 | 30.5% | 137 |

---

## 2. Evapotranspiration (FAO-56 Penman-Monteith)

| Location | ET₀ (mm/day) | Temp (°C) | Solar (kWh/m²/day) | Pulses |
|----------|-------------|-----------|-------------------|--------|
| Naivasha | 3.98 | 15.6 | 17.19 | 2-3/day |
| Kiambu | 4.31 | 18.2 | 17.19 | 4-6/day |
| Vihiga | 4.18 | 19.7 | 17.09 | 4-6/day |

---

## 3. Pest Risk with IPM + EU Export Compliance

| Location | Active Pests | Highest Risk | IPM Strategy |
|----------|-------------|-------------|-------------|
| Naivasha | Fall Armyworm (69.0, moderate) | FAW 69/100 | Pheromone traps, neem, Telenomus remus |
| Kiambu | Fall Armyworm (75.4, high) | FAW 75/100 | Pheromone traps, neem, Telenomus remus |
| Vihiga | Fall Armyworm (79.2, high) | FAW 79/100 | Pheromone traps, neem, Telenomus remus |

All three locations: EU export compliant (Regulation 2024/2004).

---

## 4. Micro-Climate Classification

| Location | Zone | Recommended Crops |
|----------|------|-------------------|
| Naivasha | Highland cool | Tea, pyrethrum, potato, wheat, high-value horticulture, rose |
| Kiambu | Highland warm | Coffee, avocado, macadamia, horticulture, maize |
| Vihiga | Highland warm | Coffee, avocado, macadamia, horticulture, maize |

---

## 5. Equatorial Benchmarking

All three locations score **Excellent (100/100)** against 4 benchmark systems:
- East Africa highlands (1500-2800m) — coffee, tea, horticulture
- West Africa savanna (200-800m) — maize, sorghum, millet
- West Africa humid (0-300m) — rice, cassava, cocoa, yam
- SE Asia lowlands (0-500m) — irrigated rice, sugarcane, palm

---

## 6. Climate Resilience Analysis

| Metric | Naivasha | Kiambu | Vihiga |
|--------|----------|--------|--------|
| Climate risk | Pest: moderate, Drought: moderate | Pest: high, Drought: high | Pest: high, Drought: high |
| Combined loss probability | 35.0% | 50.0% | 50.0% |
| Loss w/o adaptation (KES) | 35,000 | 50,000 | 50,000 |
| Cost of precision ag (KES) | 15,000 | 15,000 | 15,000 |
| Adaptation ROI | 51.7% | **116.7%** | **116.7%** |
| Disaster:adaptation ratio | **4.2:1** | **6.0:1** | **6.0:1** |

**Policy context** (per Kenya Budget Committee testimony, May 2026):
- Disaster response (2024): ~75M KES
- Climate Smart Agriculture (2026-2027): Zero-funded
- Crop insurance (2026-2027): Not allocated

---

## API Endpoints (40+ total)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Service health |
| `/ready` | GET | Readiness check |
| `/api/v1/config` | GET | System configuration |
| `/api/v1/apply` | POST | Farmer loan application |
| `/api/v1/agri/precision-farming/gdd/{lat}/{lon}/{crop}` | GET | Growing Degree Days (FAO-66) |
| `/api/v1/agri/precision-farming/et/{lat}/{lon}` | GET | Evapotranspiration (FAO-56) |
| `/api/v1/agri/precision-farming/pest-risk/{lat}/{lon}/{crop}` | GET | Pest risk with IPM |
| `/api/v1/agri/precision-farming/micro-climate/{lat}/{lon}` | GET | Micro-climate zone |
| `/api/v1/agri/precision-farming/irrigation-timing/{lat}/{lon}` | GET | Optimal irrigation timing |
| `/api/v1/agri/precision-farming/equatorial-benchmark/{lat}/{lon}` | GET | Equatorial system comparison |
| `/api/v1/agri/precision-farming/climate-resilience/{lat}/{lon}` | GET | Climate adaptation ROI |
| `/api/v1/agri/precision-farming` | POST | Full precision analysis |
| `/api/v1/agri/solar/{lat}/{lon}` | GET | Solar radiation |
| `/api/v1/agri/water/{lat}/{lon}` | GET | Water deficit |
| `/api/v1/agri/land-suitability` | POST | Land suitability analysis |
| `/api/v1/agri/market-intelligence` | POST | Market intelligence |
| `/api/v1/agri/prices/{crop}` | GET | Best crop prices |
| `/api/v1/farmers/*` | * | Farmer CRUD |
| `/api/v1/loans/*` | * | Loan management |
| `/api/v1/pools/*` | * | Securitisation pools |
| `/api/v1/payments/*` | * | Escrow lifecycle |
| `/api/v1/audit` | GET | Audit trail |

---

## Test Suite

**105 tests, all passing, zero deprecation warnings.**
- `tests/test_agents.py` — 12 tests (onboarding, geo-audit, macro-climatic, verification, credit, orchestrator)
- `tests/test_infrastructure.py` — 42 tests (settings, logging, repository, API)
- `tests/test_payments.py` — 8 tests (escrow lifecycle, MIP-003)
- `tests/test_precision_farming.py` — 29 tests (GDD, ET, pest, micro-climate, frost, irrigation, variable-rate, benchmark, resilience, constants)
- `tests/test_risk.py` — 14 tests (risk scoring, securitisation)
