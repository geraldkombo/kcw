---
name: expand-traditional-foods
description: Add new crops to TraditionalFoodsIndex with full Maundu-compliant metadata
triggers:
  - "/expand-foods"
  - "/add-crop"
  - "add traditional food"
inputs:
  crop_name: ""
  count: 1
exit_criteria:
  - "New crop entries added to knowledge/traditional_foods.py"
  - "All 117 tests still pass"
---

# Expand Traditional Foods Workflow

## Phase 1: Research
Research the crop from trusted sources:
- Patrick Maundu, *Traditional Food Plants of Kenya* (1999)
- PROTA (Plant Resources of Tropical Africa)
- FAO traditional crops database
- Kenya National Bureau of Statistics agricultural surveys
- Peer-reviewed ethnobotanical papers

For each crop, gather:
- `name_en`, `name_sw`, `scientific_name`, `local_names` (2-3)
- `status`: "indigenous" | "naturalised" | "exotic"
- `origin`: geographic origin description
- `counties`: list of Kenyan counties where found (real data only)
- `traditional_uses`: food/preparation uses
- `nutrition`: key nutritional profile
- `intercropping`: companion crops list
- `resilience_score`: float 0.0-1.0 (indigenous → higher, exotic → lower)
- `market_price_kes_tonne`: if available
- `growing_season`: months/conditions

## Phase 2: Add to Index
Add the new crop entry/entries to `KNOWLEDGE_TRADITIONAL_FOODS` list in `knowledge/traditional_foods.py`.

Follow the exact schema pattern of existing entries.

## Phase 3: Verify
Run `pytest tests/ -v -W error::DeprecationWarning` and confirm all 117 pass.

Run specific validation:
- `test_classify_indigenous_crop` — new crop is findable by name
- `test_get_crops_for_region` — new crop appears in its county results
- `test_get_crops_for_ukambani` — if applicable
