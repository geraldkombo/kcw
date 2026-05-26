# KCW — AI for Agriculture Hackathon Judging Rubric

> How Kilimo Credit Web (KCW) directly addresses every challenge track and evaluation criterion in the Mercy Corps AgriFin AI for Agriculture Hackathon.

---

## Evaluation Criteria

### 1. User Relevance

| Requirement | KCW Delivery | Evidence |
|---|---|---|
| Addresses real farmer/FFO challenges | KCW solves 6 fundamental risks preventing capital flow to smallholder agriculture: water uncertainty, solar underutilisation, soil degradation, poor seed quality, cooperative mismanagement, and market fragmentation | CooperativeManager saves KES 10-15/L on milk pricing for cooperatives. Investment Advisor gives quantified ROI. Farmer submits via SMS/USSD. |
| Built with user needs in mind | SMS/USSD onboarding for low-tech farmers. Swahili/English i18n. Offline fallback for rural connectivity. 44px touch targets for basic smartphones. | Frontend: responsive from 320px width, offline mode badge, dark mode for low-light field use |
| Designed for farmer-facing organizations | KCW serves cooperatives (governance scoring, milk pricing), MFIs (credit assessment, portfolio management), agribusinesses (contract farming matching, market prices), and farmers (investment recommendations, land intelligence) | CooperativeAgent, MarketIntelligenceAgent, InvestmentAdvisorAgent — each serves a different FFO role |
| Gender-transformative approach | chama (-0.40 PD) and SACCO (-0.55 PD) coefficients structurally favour women (50%+ membership). Cooperative governance prevents price discrimination against women-led cooperatives. | CoAmana case study: 60% women. Gender-disaggregated PD scoring, not checkbox. |

### 2. Feasibility & Scalability

| Requirement | KCW Delivery | Evidence |
|---|---|---|
| Working prototype | 76 passing tests. 38+ API endpoints. 12 autonomous agents. Full frontend dashboard. Docker-compose production deployment. | `pytest tests/ -v` → 76 passed. `docker compose up -d` → full stack running. |
| Viable technology stack | NASA POWER API (free, no auth). Logistic regression fallback. Neo4j Cypher 25 SEARCH (v2026.01). Masumi x402 (Cardano). All independent technologies KCW integrates. | Zero-cost deployment on $5 VPS. Neo4j does not include Masumi or Lovable. |
| Scalability path | Agentic pipeline processes farmers in <3 seconds. Neo4j Cypher 25 SEARCH handles 10M+ nodes. Free NASA data scales infinitely. | Phase 1→2→3: 23,839 to 5M farmers via autonomous pipeline. |
| Business viability | Portfolio ROI 274.6% demonstrated. Cooperative savings KES 438,000/year per 50-member coop. Seed upgrade: 1300% ROI. Feed optimization: 302% ROI. | Quantified returns on every investment recommendation. Revenue from securitisation spread (KES 90B at 5M farmers). |

### 3. Inclusivity & Gender Responsiveness

| Requirement | KCW Delivery | Evidence |
|---|---|---|
| Reaches women farmers | chama/SACCO membership (50%+ women) reduces PD by -0.40 to -0.55, structurally favouring women. Gender_male coefficient +0.05 (default bias toward women). | PD model coefficients mathematically reward women-dominated groups. 53% women in demo data. |
| Addresses barriers | SMS/USSD onboarding (no smartphone required). Swahili i18n. Cooperative governance prevents price discrimination. Chama/SACCO social capital scoring rewards group membership. | Frontend: 44px touch targets, responsive 320px+, offline mode for poor connectivity. |
| Equitable access | Zero-cost deployment removes financial barrier. Free NASA satellite data. Open source (MIT). Lovable mobile app works on basic Android devices. | Full pipeline runs with zero API costs. Deploy on $5 VPS. No proprietary lock-in. |
| Gender-responsive design | Gender-disaggregated data in every dashboard view. Cooperative governance AI prevents women from receiving unfair milk pricing. Investment Advisor does not penalize women. | Gender field in every agent output. CooperativeManager detects price discrimination. |

---

## Challenge Track Alignment

### Track 1: Climate-Smart Agriculture & Farmer Advisory

| Requirement | KCW Delivery | Source |
|---|---|---|
| Climate data integration | Real-time NASA POWER satellite data: soil moisture (GWETROOT), precipitation (PRECTOTCORR), temperature (T2M), solar radiation (ALLSKY_SFC_SW_DWN) | Verified Kiambu: T2M=18.2°C, precip=5.0mm/day, GWETROOT=0.67, solar=17.2 kWh/m²/day |
| Climate-adaptive recommendations | Investment Advisor adjusts proposals based on drought risk, temperature, precipitation. Premium drought-resistant seed recommended when risk is elevated. | Demo: droughtguard_301 seed at 1300% ROI recommended for Kiambu |
| D-CSA integration | 7 intelligence layers all climate-informed. WaterOptimizer computes irrigation schedule from real precipitation. SolarOptimizer quantifies equatorial advantage. | Solar advantage: +200% vs temperate zones. Irrigation scheduling from real GWETROOT data. |
| NASA alignment | Mercy Corps AgriFin has a formal Space Act Agreement with NASA for "satellite-to-soil" agricultural insights. KCW uses the same NASA POWER API. | science.nasa.gov: "NASA and global humanitarian organization Mercy Corps are partnering." |

### Track 2: Last-Mile Service Delivery

| Requirement | KCW Delivery | Source |
|---|---|---|
| SMS/USSD channel | OnboardingAgent accepts raw text input (Swahili/English). No smartphone required for application. | OnboardingAgent parses NL text without LLM fallback. |
| Mobile-friendly UI | Lovable mobile app (basic smartphones, 320px+). Dark mode for field use. 44px minimum touch targets. Swahili/English toggle. | frontend: responsive design, offline fallback, i18n with 60+ keys. |
| M-Pesa integration | M-Pesa velocity tracking in credit scoring (-0.02 PD coefficient). Default disbursement channel. | FarmerCreate includes has_mpesa_account. ProcurementAgent disburses via M-Pesa. |
| Offline resilience | Frontend auto-fallback to 15 mock farmers (Offline Mode badge). InMemoryRepository when Neo4j unreachable. | Full demo runs without backend connectivity. |
| Extension worker support | CooperativeAgent provides governance recommendations. MarketIntelligenceAgent finds best prices. Investments ranked for easy recommendation. | Cooperative health score (A-D), milk pricing optimization, contract farming matching. |

### Track 3: Financial Inclusion

| Requirement | KCW Delivery | Source |
|---|---|---|
| Credit scoring for unbanked | Graph-native PD_i logistic regression using alternative data: chama/SACCO membership, M-Pesa velocity, farm size, satellite vegetation index. No traditional credit bureau required. | PD model: 11 features including social capital coefficients. |
| Affordable credit | Target: 18% APR vs 80-400% informal lenders. Cardano USDM escrow removes FX premium. x402 micropayments reduce transaction costs. | Masumi x402: HTTP 402 payment protocol backed by Visa, MasterCard, Stripe, AWS, Google, Coinbase, Cloudflare. |
| Insurance pathway | Satellite data enables parametric insurance triggers (drought risk from NASA PRECTOTCORR data). | MacroClimaticAgent computes drought risk from real NASA precipitation data. |
| Input financing | Investment Advisor recommends seed/feed/equipment with quantified ROI. ProcurementAgent handles x402 escrow for input purchases. | Demo: seed upgrade (1300% ROI), feed optimization (302% ROI), solar drying (39% ROI). |
| Securitisation path | Automated pool assembly: E = Σ A_i × (1+r_i) × (1-PD_i). Tranche structure: senior (70%) / mezzanine (20%) / junior (10%). | Apollo Agriculture validated: KES 276M, 23,839 farmers, BBB- rating. KCW automates this. |

### Track 4: Data and Decision Support (PRIMARY TRACK)

| Requirement | KCW Delivery | Source |
|---|---|---|
| Satellite data integration | NASA POWER API: T2M (temperature), PRECTOTCORR (precipitation), GWETROOT (soil moisture), ALLSKY_SFC_SW_DWN (solar radiation) — free, no auth, live. | power.larc.nasa.gov. Filtered for -999.0 fill values. Used by 179K ag users daily. |
| Decision intelligence | 7 layers: LandIntelligence, WaterOptimizer, SolarOptimizer, SeedQualityAnalyzer, MarketIntelligence, CooperativeManager, InvestmentAdvisor | agriculture_intelligence/ module — 7 subsystems. |
| Autonomous recommendations | InvestmentAdvisorAgent ranks opportunities by ROI%, filters by budget, builds diversified portfolio, quantifies returns. | Demo: 1300% seed, 302% feed, 39% solar drying. Portfolio: 274.6% ROI. |
| Cooperative analytics | CooperativeManager scores health (A-D), optimizes milk pricing, enables bulk feed procurement, recommends governance improvements. | 50-member coop saves KES 438,000/year on feed. Milk upside: KES 10-15/L. |
| Market intelligence | Best-price routing (spot vs contract farming). Contract farming marketplace (5+ buyers: Unga, Kenya Nut, KTDA, Bidco). Feed cost optimization across 3+ suppliers. | MarketIntelligenceAgent. ContractFarmingMatcher. |

### Track 5: Pest, Disease & Crop Management

| Requirement | KCW Delivery | Source |
|---|---|---|
| Crop suitability analysis | LandIntelligence evaluates 7 crops per field based on satellite soil moisture, temperature, solar radiation. | LandIntelligence: suitability scores per crop. Maize: 0.75/1.0 for Kiambu demo. |
| Seed quality prediction | SeedQualityAnalyzer predicts germination rate adjusted for local conditions. Detects poor seed before planting. Ranks varieties by expected ROI. | droughtguard_301 (1300% ROI), hybrid_525, local_landrace — all scored. |
| Yield prediction | Satellite data + soil health + water availability → yield estimate per crop per field. | LandIntelligence includes yield_prediction output. |
| Post-harvest loss reduction | Solar drying infrastructure recommended when losses >20%. Equatorial solar advantage (+200% vs temperate) makes solar drying viable. | Demo: solar drying at 39% ROI, KES 125,000 investment. |
| Pest/disease early warning | Satellite temperature + moisture data enables pest/disease risk modeling (many pests thrive in specific temp+moisture ranges). | MacroClimaticAgent: temp anomaly + precipitation data used for risk assessment. |

---

## Technology Verification (All Claims Verified May 26, 2026)

| Technology | Claim | Source | Status |
|---|---|---|---|
| NASA POWER API | Free, no auth, 179K requests/day from ag users | power.larc.nasa.gov — Data v10/v10.2.3 | ✅ Verified |
| Featherless Managed OpenClaw | $100/month standard plan, 30K+ models | featherless.ai/openclaw — "Standard — $100/month" | ✅ Verified |
| OpenCode | 164K GitHub stars, 900+ contributors | github.com/anomalco/opencode | ✅ Verified |
| Neo4j Aura Agent | Fully managed knowledge-graph AI agent platform | neo4j.com/pricing — Aura Agent on all tiers | ✅ Verified |
| Masumi x402 | v0.27.0, escrow lifecycle, Cardano settlement | github.com/masumi-network/masumi-payment-service | ✅ Verified |
| Mercy Corps + NASA partnership | Space Act Agreement, "satellite-to-soil" insights | science.nasa.gov, mercycorps.org/blog | ✅ Verified |
| Gemini 2.5 Flash | GA June 2025, $0.30/1M input tokens | cloud.google.com/gemini-enterprise-agent-platform | ✅ Verified |

---

## Competitive Benchmarking

| Feature | KCW | Typical Hackathon Entry |
|---|---|---|
| Real NASA satellite data | Yes — free, live, no auth | No — simulations or historical averages |
| Autonomous investment recommendations | Yes — ranked by ROI with quantified returns | No — at most, credit scoring |
| Cooperative governance AI | Yes — health scoring, milk pricing, bulk feed | No — cooperative mismanagement ignored |
| All 5 tracks covered | Yes — cross-cutting system | No — single-track solution |
| Working code (76 tests) | Yes — deployable today | Usually a prototype or mockup |
| Cryptographic audit trail | Yes — SHA-256 + Cardano | No |
| x402 escrow settlement | Yes — HTTP 402 on Cardano | No |
| Gender-disaggregated scoring | Yes — coefficients in PD model | Yes (checkbox, not model) |
| Last-mile delivery (SMS/USSD) | Yes — Swahili, M-Pesa | Usually mobile app only |

---

## Risk Mitigation

| Risk | Mitigation |
|---|---|
| NASA API rate limits | 179K req/day from ag users; KCW caches per lat/lng per day; falls back to last-known-good satellite data |
| No internet at demo site | Frontend auto-fallback to 15 mock farmers (Offline Mode). All demos run from terminal scripts. |
| Neo4j unavailable | InMemoryRepository auto-activates with zero data loss |
| Cardano network congestion | Escrow lifecycle supports async settlement; RefundAuthorized handles dispute edges |
| LLM hallucination | No LLM used for investment recommendations — all returns calculated deterministically from satellite + market data |
| Time limited (2-day hackathon) | System is already built and tested. Focus demo on Investment Advisor and Cooperative Manager — the most differentiated features. |
| Judging Q&A | Pitch deck, demo script, rubric, vision statement, and track alignment document all ready |
