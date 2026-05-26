# Lovable MCP Dashboard Prompt
Use this prompt with Lovable MCP Server (Research Preview, May 7, 2026)
to generate the KCW farmer dashboard.

Tools: create_project, deploy_project, send_message, get_project

## Prompt:

"Create a single-page web dashboard for Kilimo Credit Web (KCW), an
agricultural lending platform for Kenyan smallholder farmers. Use:
- Tailwind CSS CDN for styling
- Chart.js CDN for visualisations
- Africa-themed colour palette (green #2E7D32, gold #FFB300, earth #5D4037)

The backend API runs separately at the URL set in `API_BASE` variable.
Default `API_BASE = 'http://localhost:8000'` — change to your Render URL.

## Pages:

### 1. Dashboard (`/`)
- KPI cards: farmers onboarded, active loans, portfolio volume KES, pools created
- Kenya county SVG dot-density map (circle size = farmer density)
- Loan portfolio pie chart (seeds, fertiliser, equipment, irrigation, livestock, transport)
- "Offline Mode" badge when API unreachable

### 2. Farmers (`/farmers`)
- Searchable table: ID, Name, County, Crop, Farm Size (ha), Credit Score, PD (%), Status
- Colour-coded badges: green (active), red (defaulted), gold (pending), blue (approved)
- Filter by county dropdown + status dropdown
- Detail drawer/modal on row click showing audit trail entries

### 3. Credit Assessment (`/assess`)
- Form fields: first_name, last_name, phone, gender (M/F dropdown), county,
  sub_county, farm_size_ha, primary_crop, chama_member checkbox, sacco_member checkbox
- Submit calls POST {API_BASE}/api/v1/apply
- Result card: approved/declined badge, credit score (0-100), PD%, max loan KES,
  risk factor breakdown list with direction arrows

### 4. Securitisation Pools (`/pools`)
- Cards showing: farmer count, total notional KES, avg PD%, expected revenue, rating
- Button "Build Pool from Approved Farmers" calls POST {API_BASE}/api/v1/pools/build
- Detail expand showing individual farmer contributions

### 5. x402 Payments (`/payments`)
- Escrow timeline with colour-coded state badges
- Create escrow form (amount, description)
- Last 3 transactions with state machine transitions

### 6. Precision Farming (`/precision-farming`)
- Input: lat/lon + crop dropdown (maize, beans, coffee, tea, kale, avocado, tomato)
- Fetch all precision farming endpoints on submit, display:
  - **GDD Card** — growing degree days value with equatorial benchmark comparison
  - **Pest Risk Card** — table of detected pests with risk level badges, IPM recommendations
  - **EU Export Compliance** — compliant/not-compliant badge, list of elevated risk items
  - **Micro-Climate Zone** — zone name with description and recommended crops
  - **Frost Risk Card** — risk level with protective measures
  - **Irrigation Timing** — optimal time with reasoning
  - **Climate Resilience Card** — adaptation ROI%, disaster response vs adaptation ratio,
    net savings from precision agriculture, policy quote from Kenya Budget Committee testimony

## Technical Notes:
- API_BASE as a constant at the top of the script
- All fetch URLs use API_BASE + path (no hardcoded localhost)
- 15 mock farmers for offline fallback when fetch fails
- Mobile-first responsive (320px min-width), 44px touch targets
- Dark mode toggle with localStorage persistence
- English + Swahili i18n toggle
- Toast notifications for errors and successes
- Under 500KB total bundle"
