"""Traditional food plants of Kenya — knowledge layer grounded in traditional food knowledge research.

Sources:
  - Traditional food knowledge — Kenya AI Challenge workshop (2026)
  - Ojwang, H.J. (2020). Pedagogical Value of Indigenous Knowledge for Food Security:
    Learning from Women Farmers in Homa Bay County, Kenya. PhD Thesis, University of Nairobi.
  - Maundu, Ngugi & Kabuye (1999). Traditional Food Plants of Kenya. NMK. [493 citations]
  - Maundu et al. (2009). Biodiversity of African Vegetables. In African Indigenous Vegetables in Urban Agriculture.
  - Kennedy, Wang, Maundu & Hunter (2022). The role of traditional knowledge and food biodiversity
    to transform modern food systems. Trends in Food Science & Technology, 130, 32-41.
  - Maundu et al. (2005). Useful Trees and Shrubs for Kenya. ICRAF.
  - NMK Traditional Food Plants Database

Key insight (Kenya AI Challenge workshop, 2026):
  Only ~1/3 of Nairobi's ~680 traditional foods originate in Kenya.
  The rest is "exotic" — introduced from elsewhere in Africa or the world.
  Every community brings distinct food crops → this drives real market demand.
"""

from __future__ import annotations

CropClassification = dict


class TraditionalFoodsIndex:
    """Knowledge layer referencing Maundu et al.'s traditional food plants research.

    Classifies crops as indigenous (originated in East Africa), naturalised
    (introduced but fully integrated), or exotic (recent introduction, high-input).
    Provides origin, growing regions, traditional uses, market channels, and
    intercropping patterns. Used to enrich agent recommendations with local
    food system context.
    """

    CROP_INDEX = {
        "amaranth": {
            "name_sw": "terere/mchicha",
            "name_en": "Amaranth / African spinach",
            "origin": "East Africa (multiple species: A. cruentus, A. hybridus, A. dubius)",
            "status": "indigenous",
            "resilience_score": 0.92,
            "regions": ["Kisumu", "Homa Bay", "Migori", "Siaya", "Busia", "Vihiga", "Kakamega", "Bungoma", "Machakos", "Kitui", "Makueni"],
            "traditional_uses": "Leafy vegetable steamed or boiled, served with ugali. Seeds used as grain porridge.",
            "nutrition": "High iron (5.2mg/100g), calcium (215mg/100g), vitamin A, protein (4.6g/100g). Superior to exotic spinach.",
            "gdd_base_temp": 15,
            "gdd_harvest": 600,
            "temp_range": (18, 32),
            "precip_range": (2.0, 6.0),
            "soil_moisture_min": 0.2,
            "growing_days": 45,
            "water_need_mm": 200,
            "market_price_kes_tonne": 60000,
            "intercropping": ["maize", "beans", "cowpea"],
            "market_demand": "High year-round in urban centres. Ethnic food corridors from Lake Region to Nairobi.",
        },
        "spider_plant": {
            "name_sw": "sagaa/mnavu/mlenda",
            "name_en": "Spider plant / African cabbage / Cat's whiskers",
            "origin": "East and Southern Africa (Cleome gynandra)",
            "status": "indigenous",
            "resilience_score": 0.85,
            "regions": ["Kisumu", "Siaya", "Homa Bay", "Migori", "Busia", "Vihiga", "Kakamega", "Bungoma", "Nandi", "Kericho"],
            "traditional_uses": "Leafy vegetable with distinctive bitter taste. Usually steamed or boiled in milk/soured milk.",
            "nutrition": "High beta-carotene, vitamin C, calcium, iron. Bitter compounds (glucosinolates) have antimicrobial properties.",
            "gdd_base_temp": 15,
            "gdd_harvest": 550,
            "temp_range": (18, 30),
            "precip_range": (2.5, 5.5),
            "soil_moisture_min": 0.25,
            "growing_days": 40,
            "water_need_mm": 180,
            "market_price_kes_tonne": 65000,
            "intercropping": ["maize", "cassava", "sorghum"],
            "market_demand": "High in Luo and Luhya communities. Strong Nairobi demand via Kisumu-Nairobi buses.",
        },
        "black_nightshade": {
            "name_sw": "managu/osusu/mnavu",
            "name_en": "Black nightshade / African nightshade",
            "origin": "East Africa (Solanum nigrum complex, S. scabrum)",
            "status": "indigenous",
            "resilience_score": 0.88,
            "regions": ["Kisumu", "Homa Bay", "Siaya", "Migori", "Busia", "Kakamega", "Bungoma", "Vihiga", "Kiambu", "Murang'a", "Nyeri", "Meru"],
            "traditional_uses": "Most popular traditional leafy vegetable. Leaves steamed/boiled, sometimes with milk or groundnut paste.",
            "nutrition": "Very high iron (7.8mg/100g), vitamin A, vitamin C, calcium. Anti-inflammatory compounds.",
            "gdd_base_temp": 14,
            "gdd_harvest": 500,
            "temp_range": (16, 28),
            "precip_range": (3.0, 6.0),
            "soil_moisture_min": 0.3,
            "growing_days": 35,
            "water_need_mm": 160,
            "market_price_kes_tonne": 70000,
            "intercropping": ["maize", "banana", "beans", "cassava"],
            "market_demand": "Highest demand traditional vegetable in Nairobi. Multiple ethnic groups consume it.",
        },
        "cowpea_leaves": {
            "name_sw": "kunde/choroko",
            "name_en": "Cowpea leaves",
            "origin": "East and West Africa (Vigna unguiculata)",
            "status": "indigenous",
            "resilience_score": 0.95,
            "regions": ["Machakos", "Kitui", "Makueni", "Kilifi", "Kwale", "Taita Taveta", "Kajiado", "Narok", "Meru", "Tharaka Nithi"],
            "traditional_uses": "Leaves picked, chopped, steamed. Often cooked with tomatoes, onions, coconut milk in coastal regions.",
            "nutrition": "High protein (4.7g/100g leaves, 24g/100g grain), iron, folate. Dual-purpose crop (leaves + grain).",
            "gdd_base_temp": 12,
            "gdd_harvest": 700,
            "temp_range": (18, 35),
            "precip_range": (1.5, 5.0),
            "soil_moisture_min": 0.15,
            "growing_days": 60,
            "water_need_mm": 250,
            "market_price_kes_tonne": 55000,
            "intercropping": ["maize", "sorghum", "millet", "cassava"],
            "market_demand": "High in dryland counties. Drought-tolerant, ideal for ASAL regions.",
        },
        "jute_mallow": {
            "name_sw": "mrenda/murere/apoth",
            "name_en": "Jute mallow / Jew's mallow",
            "origin": "East Africa (Corchorus olitorius, C. tridens)",
            "status": "indigenous",
            "resilience_score": 0.78,
            "regions": ["Kisumu", "Siaya", "Homa Bay", "Migori", "Busia", "Vihiga", "Kakamega", "Bungoma"],
            "traditional_uses": "Slimy/mucilaginous leaves cooked as vegetable. Important in Luo and Luhya cuisine.",
            "nutrition": "High fibre, beta-carotene, vitamin E, calcium. Mucilage aids digestion.",
            "gdd_base_temp": 16,
            "gdd_harvest": 550,
            "temp_range": (20, 35),
            "precip_range": (2.5, 6.0),
            "soil_moisture_min": 0.25,
            "growing_days": 40,
            "water_need_mm": 200,
            "market_price_kes_tonne": 58000,
            "intercropping": ["cassava", "sweet_potato", "sorghum"],
            "market_demand": "Moderate but consistent. Ethnic demand from Luo & Luhya diaspora in Nairobi.",
        },
        "pumpkin_leaves": {
            "name_sw": "majani ya malenge/murenda",
            "name_en": "Pumpkin leaves",
            "origin": "East Africa (Cucurbita moschata — African landraces)",
            "status": "indigenous",
            "resilience_score": 0.80,
            "regions": ["Kisumu", "Homa Bay", "Siaya", "Vihiga", "Kakamega", "Busia", "Bungoma", "Migori", "Kiambu", "Murang'a", "Machakos"],
            "traditional_uses": "Young shoots and leaves harvested as vegetable. Fruit also consumed.",
            "nutrition": "High vitamin A, iron, calcium. Seeds rich in zinc and healthy fats.",
            "gdd_base_temp": 15,
            "gdd_harvest": 800,
            "temp_range": (18, 32),
            "precip_range": (2.0, 5.5),
            "soil_moisture_min": 0.2,
            "growing_days": 60,
            "water_need_mm": 250,
            "market_price_kes_tonne": 50000,
            "intercropping": ["maize", "beans", "cassava", "sorghum"],
            "market_demand": "Widespread across communities. Both leaves and fruit have market value.",
        },
        "finger_millet": {
            "name_sw": "wimbi/ugali",
            "name_en": "Finger millet",
            "origin": "East Africa (Eleusine coracana) — domesticated in Uganda/Ethiopia highlands",
            "status": "indigenous",
            "resilience_score": 0.85,
            "regions": ["Uasin Gishu", "Nandi", "Kericho", "Elgeyo Marakwet", "West Pokot", "Baringo", "Laikipia", "Meru", "Embu", "Tharaka Nithi"],
            "traditional_uses": "Flour for ugali, porridge. Fermented for beverages.",
            "nutrition": "Very high calcium (344mg/100g), iron (3.9mg/100g), fibre. Low glycemic index.",
            "gdd_base_temp": 10,
            "gdd_harvest": 1400,
            "temp_range": (18, 30),
            "precip_range": (2.5, 6.0),
            "soil_moisture_min": 0.2,
            "growing_days": 120,
            "water_need_mm": 350,
            "market_price_kes_tonne": 65000,
            "intercropping": ["beans", "cowpea", "pigeon_pea", "sorghum"],
            "market_demand": "Growing health food demand in urban centres. Premium price vs maize.",
        },
        "sorghum": {
            "name_sw": "mtama",
            "name_en": "Sorghum",
            "origin": "East Africa (Sorghum bicolor) — primary domestication centre in Ethiopia/Sudan",
            "status": "indigenous",
            "resilience_score": 0.90,
            "regions": ["Machakos", "Kitui", "Makueni", "Kilifi", "Kwale", "Taita Taveta", "Kajiado", "Narok", "Baringo", "Laikipia", "Isiolo", "Meru"],
            "traditional_uses": "Ugali, porridge, fermented beverages. Important food security crop in ASALs.",
            "nutrition": "High protein (11g/100g), iron, zinc, fibre. Gluten-free.",
            "gdd_base_temp": 10,
            "gdd_harvest": 1400,
            "temp_range": (20, 38),
            "precip_range": (1.5, 5.0),
            "soil_moisture_min": 0.1,
            "growing_days": 120,
            "water_need_mm": 350,
            "market_price_kes_tonne": 45000,
            "intercropping": ["cowpea", "pigeon_pea", "millet", "cassava"],
            "market_demand": "High in ASAL counties. Brewing industry demand. Growing gluten-free market.",
        },
        "pigeon_pea": {
            "name_sw": "mbaazi/njahi",
            "name_en": "Pigeon pea / Gongo pea",
            "origin": "East Africa (Cajanus cajan) — secondary domestication centre in East Africa",
            "status": "indigenous",
            "resilience_score": 0.88,
            "regions": ["Machakos", "Kitui", "Makueni", "Kilifi", "Kwale", "Taita Taveta", "Homa Bay", "Migori", "Meru", "Tharaka Nithi"],
            "traditional_uses": "Green seeds boiled as vegetable. Dried split used in stews.",
            "nutrition": "High protein (21g/100g), fibre, folate, magnesium. Nitrogen-fixing.",
            "gdd_base_temp": 12,
            "gdd_harvest": 1800,
            "temp_range": (18, 35),
            "precip_range": (1.5, 5.0),
            "soil_moisture_min": 0.1,
            "growing_days": 150,
            "water_need_mm": 400,
            "market_price_kes_tonne": 70000,
            "intercropping": ["sorghum", "millet", "maize", "cassava"],
            "market_demand": "High in dryland counties. Nitrogen fixation reduces fertiliser cost.",
        },
        "bambara_nut": {
            "name_sw": "njugu mawe/nyimo",
            "name_en": "Bambara groundnut",
            "origin": "Naturalised in East Africa over centuries (Vigna subterranea)",
            "status": "naturalised",
            "resilience_score": 0.85,
            "regions": ["Kilifi", "Kwale", "Taita Taveta", "Machakos", "Kitui", "Makueni", "Homa Bay", "Migori", "Busia"],
            "traditional_uses": "Seeds boiled with salt, roasted, or pounded into flour.",
            "nutrition": "High protein (19g/100g), fibre, iron, potassium. Drought-tolerant.",
            "gdd_base_temp": 14,
            "gdd_harvest": 1500,
            "temp_range": (20, 35),
            "precip_range": (2.0, 5.0),
            "soil_moisture_min": 0.15,
            "growing_days": 130,
            "water_need_mm": 350,
            "market_price_kes_tonne": 80000,
            "intercropping": ["sorghum", "millet", "cassava", "maize"],
            "market_demand": "Moderate but growing as climate-resilient crop.",
        },
        "cassava": {
            "name_sw": "muhogo/mihogo",
            "name_en": "Cassava",
            "origin": "Naturalised in East Africa for >300 years (Manihot esculenta)",
            "status": "naturalised",
            "resilience_score": 0.92,
            "regions": ["Busia", "Kakamega", "Bungoma", "Vihiga", "Siaya", "Kisumu", "Homa Bay", "Migori", "Kilifi", "Kwale", "Taita Taveta", "Machakos", "Kitui"],
            "traditional_uses": "Boiled, fried, dried into flour. Leaves cooked as vegetable.",
            "nutrition": "High energy. Leaves rich in protein, vitamin A, iron.",
            "gdd_base_temp": 15,
            "gdd_harvest": 2400,
            "temp_range": (18, 35),
            "precip_range": (2.0, 7.0),
            "soil_moisture_min": 0.15,
            "growing_days": 300,
            "water_need_mm": 800,
            "market_price_kes_tonne": 25000,
            "intercropping": ["maize", "beans", "cowpea", "pumpkin_leaves", "jute_mallow"],
            "market_demand": "High year-round in Lake Region and Coast. Dual-purpose crop.",
        },
        "sweet_potato": {
            "name_sw": "kiazi tamu/mbambara",
            "name_en": "Sweet potato",
            "origin": "Centuries of cultivation in East Africa (Ipomoea batatas)",
            "status": "naturalised",
            "resilience_score": 0.82,
            "regions": ["Busia", "Kakamega", "Bungoma", "Vihiga", "Siaya", "Kisumu", "Homa Bay", "Migori", "Meru", "Embu", "Tharaka Nithi", "Machakos", "Kilifi"],
            "traditional_uses": "Roots boiled, roasted, or fried. Leaves consumed as vegetable.",
            "nutrition": "Orange-fleshed: very high beta-carotene. Good source of vitamin C, potassium.",
            "gdd_base_temp": 12,
            "gdd_harvest": 1200,
            "temp_range": (15, 30),
            "precip_range": (2.5, 6.0),
            "soil_moisture_min": 0.2,
            "growing_days": 120,
            "water_need_mm": 350,
            "market_price_kes_tonne": 35000,
            "intercropping": ["maize", "beans", "cassava", "sorghum"],
            "market_demand": "High year-round. OFSP promoted for vitamin A deficiency.",
        },
        "yam": {
            "name_sw": "kiasi/mayuni/nduma",
            "name_en": "Yellow yam / African yam",
            "origin": "Naturalised in East Africa (Dioscorea cayenensis, D. alata)",
            "status": "naturalised",
            "resilience_score": 0.78,
            "regions": ["Busia", "Kakamega", "Bungoma", "Vihiga", "Siaya", "Kisumu", "Homa Bay", "Meru", "Tharaka Nithi", "Kilifi"],
            "traditional_uses": "Roots boiled or roasted. Important ceremonial food.",
            "nutrition": "Good energy source, potassium, vitamin C.",
            "gdd_base_temp": 18,
            "gdd_harvest": 2000,
            "temp_range": (20, 34),
            "precip_range": (3.0, 7.0),
            "soil_moisture_min": 0.3,
            "growing_days": 240,
            "water_need_mm": 700,
            "market_price_kes_tonne": 45000,
            "intercropping": ["maize", "cassava", "banana", "beans"],
            "market_demand": "Moderate. Higher price point. Valued by specific communities.",
        },
        "baobab": {
            "name_sw": "mbuyu/buyu",
            "name_en": "Baobab",
            "origin": "East Africa — indigenous to African savanna (Adansonia digitata)",
            "status": "indigenous",
            "resilience_score": 1.00,
            "regions": ["Kilifi", "Kwale", "Taita Taveta", "Kitui", "Makueni", "Machakos", "Kajiado", "Narok", "Laikipia"],
            "traditional_uses": "Fruit pulp mixed with water/porridge. Leaves as vegetable.",
            "nutrition": "Extremely high vitamin C (6x orange), calcium, potassium, antioxidants.",
            "gdd_base_temp": 20,
            "gdd_harvest": 3650,
            "temp_range": (20, 40),
            "precip_range": (1.0, 4.0),
            "soil_moisture_min": 0.05,
            "growing_days": 365,
            "water_need_mm": 500,
            "market_price_kes_tonne": 150000,
            "intercropping": ["sorghum", "millet", "cowpea"],
            "market_demand": "Growing export demand (superfood). Local demand in ASAL counties.",
        },
        "tamarind": {
            "name_sw": "ukwaju",
            "name_en": "Tamarind",
            "origin": "East Africa — indigenous to African savanna (Tamarindus indica)",
            "status": "indigenous",
            "resilience_score": 0.94,
            "regions": ["Kilifi", "Kwale", "Taita Taveta", "Kitui", "Makueni", "Machakos", "Kajiado", "Narok", "Isiolo", "Garissa"],
            "traditional_uses": "Fruit pulp used in juice, chutney, stews.",
            "nutrition": "High in B vitamins, calcium, potassium, magnesium.",
            "gdd_base_temp": 20,
            "gdd_harvest": 3650,
            "temp_range": (22, 40),
            "precip_range": (1.0, 4.0),
            "soil_moisture_min": 0.05,
            "growing_days": 365,
            "water_need_mm": 400,
            "market_price_kes_tonne": 80000,
            "intercropping": ["sorghum", "millet", "cowpea"],
            "market_demand": "Growing juice industry demand. Drought-hardy tree.",
        },
        # ── Additional indigenous vegetables (Ojwang, 2020 — Homa Bay County) ──
        "dek": {
            "name_sw": "dek",
            "name_en": "Dek / Luo traditional leafy vegetable",
            "origin": "East Africa — traditional Luo vegetable, Homa Bay County",
            "status": "indigenous",
            "resilience_score": 0.82,
            "regions": ["Homa Bay", "Kisumu", "Siaya", "Migori", "Busia", "Vihiga", "Kakamega", "Bungoma"],
            "traditional_uses": "Leafy vegetable steamed or boiled, served with ugali. Wild-harvested and semi-cultivated.",
            "nutrition": "High iron, beta-carotene, calcium. Typical of indigenous dark leafy vegetables.",
            "gdd_base_temp": 15,
            "gdd_harvest": 500,
            "temp_range": (18, 32),
            "precip_range": (2.5, 6.0),
            "soil_moisture_min": 0.2,
            "growing_days": 35,
            "water_need_mm": 180,
            "market_price_kes_tonne": 55000,
            "intercropping": ["maize", "cassava", "beans", "sweet_potato"],
            "market_demand": "Moderate, ethnic demand from Luo communities in Nairobi and Lake Region.",
        },
        "mito": {
            "name_sw": "mito",
            "name_en": "Mito / Luo indigenous vegetable",
            "origin": "East Africa — traditional Luo vegetable",
            "status": "indigenous",
            "resilience_score": 0.82,
            "regions": ["Homa Bay", "Kisumu", "Siaya", "Migori", "Busia", "Kakamega"],
            "traditional_uses": "Leafy vegetable steamed with tomatoes. Gathered from wild or farmed in home gardens.",
            "nutrition": "High vitamin A, iron, and fibre. Comparable to spider plant in mineral content.",
            "gdd_base_temp": 15,
            "gdd_harvest": 550,
            "temp_range": (18, 30),
            "precip_range": (2.5, 5.5),
            "soil_moisture_min": 0.25,
            "growing_days": 40,
            "water_need_mm": 200,
            "market_price_kes_tonne": 52000,
            "intercropping": ["cassava", "maize", "sorghum", "beans"],
            "market_demand": "Low-moderate but stable among Luo diaspora. Limited market integration.",
        },
        "boo": {
            "name_sw": "boo",
            "name_en": "Boo / Luo leafy vegetable",
            "origin": "East Africa — traditional Luo vegetable",
            "status": "indigenous",
            "resilience_score": 0.80,
            "regions": ["Homa Bay", "Kisumu", "Siaya", "Migori", "Busia"],
            "traditional_uses": "Leaves steamed or boiled. Valued for its slightly bitter taste and nutritional density.",
            "nutrition": "Rich in iron, calcium, and antioxidants. Bitter compounds support digestive health.",
            "gdd_base_temp": 14,
            "gdd_harvest": 600,
            "temp_range": (16, 30),
            "precip_range": (2.0, 5.5),
            "soil_moisture_min": 0.2,
            "growing_days": 45,
            "water_need_mm": 220,
            "market_price_kes_tonne": 50000,
            "intercropping": ["maize", "cassava", "sorghum", "cowpea"],
            "market_demand": "Ethnic niche market. Sold in Kawangware and Kibera markets in Nairobi.",
        },
        "atipa": {
            "name_sw": "atipa",
            "name_en": "Atipa / Luo wild vegetable",
            "origin": "East Africa — wild-harvested Luo vegetable, Homa Bay County",
            "status": "indigenous",
            "resilience_score": 0.78,
            "regions": ["Homa Bay", "Migori", "Siaya", "Kisumu", "Busia"],
            "traditional_uses": "Wild-harvested leafy vegetable from lake-side areas. Often cooked with soda to soften.",
            "nutrition": "Good source of vitamin A, iron, and zinc. Higher mineral content than exotic greens.",
            "gdd_base_temp": 16,
            "gdd_harvest": 450,
            "temp_range": (18, 32),
            "precip_range": (3.0, 6.0),
            "soil_moisture_min": 0.25,
            "growing_days": 30,
            "water_need_mm": 160,
            "market_price_kes_tonne": 48000,
            "intercropping": ["cassava", "sweet_potato", "banana"],
            "market_demand": "Small but steady ethnic demand. Seasonal availability in Lake Region markets.",
        },
        "odielo": {
            "name_sw": "odielo",
            "name_en": "Odielo / Luo indigenous vegetable",
            "origin": "East Africa — traditional Luo vegetable",
            "status": "indigenous",
            "resilience_score": 0.82,
            "regions": ["Homa Bay", "Kisumu", "Siaya", "Migori", "Vihiga"],
            "traditional_uses": "Slightly mucilaginous leaves, cooked with tomatoes and onions. Used in traditional Luo cuisine.",
            "nutrition": "High fibre, beta-carotene, calcium. Similar nutritional profile to jute mallow.",
            "gdd_base_temp": 15,
            "gdd_harvest": 500,
            "temp_range": (18, 32),
            "precip_range": (2.5, 6.0),
            "soil_moisture_min": 0.2,
            "growing_days": 35,
            "water_need_mm": 180,
            "market_price_kes_tonne": 53000,
            "intercropping": ["maize", "cassava", "beans"],
            "market_demand": "Moderate ethnic demand. Increasing awareness among Nairobi health-conscious consumers.",
        },
        "ndemra": {
            "name_sw": "ndemra",
            "name_en": "Ndemra / Luo indigenous vegetable",
            "origin": "East Africa — traditional Luo vegetable, Homa Bay",
            "status": "indigenous",
            "resilience_score": 0.85,
            "regions": ["Homa Bay", "Siaya", "Kisumu", "Migori", "Busia"],
            "traditional_uses": "Leaves cooked as vegetable. Known for drought tolerance and ease of cultivation.",
            "nutrition": "High iron, protein, and vitamin C. Good mineral density compared to exotic greens.",
            "gdd_base_temp": 14,
            "gdd_harvest": 550,
            "temp_range": (16, 34),
            "precip_range": (2.0, 5.5),
            "soil_moisture_min": 0.15,
            "growing_days": 40,
            "water_need_mm": 200,
            "market_price_kes_tonne": 51000,
            "intercropping": ["sorghum", "cowpea", "cassava", "millet"],
            "market_demand": "Moderate in Lake Region markets. Drought tolerance makes it a food security crop.",
        },
        "alikra": {
            "name_sw": "alikra",
            "name_en": "Alikra / Luo leafy vegetable",
            "origin": "East Africa — traditional Luo vegetable",
            "status": "indigenous",
            "resilience_score": 0.80,
            "regions": ["Homa Bay", "Migori", "Kisumu", "Siaya", "Kakamega"],
            "traditional_uses": "Leaves steamed, often mixed with other indigenous vegetables. Valued for flavour and nutrition.",
            "nutrition": "Good source of vitamins A, C, and iron. Comparable to amaranth in nutritional density.",
            "gdd_base_temp": 15,
            "gdd_harvest": 500,
            "temp_range": (18, 32),
            "precip_range": (2.5, 6.0),
            "soil_moisture_min": 0.2,
            "growing_days": 35,
            "water_need_mm": 180,
            "market_price_kes_tonne": 54000,
            "intercropping": ["maize", "cassava", "beans", "sweet_potato"],
            "market_demand": "Moderate. Sold in rural and peri-urban markets of Lake Region.",
        },
        # ── Traditional grain (Ojwang, 2020) ──
        "ng_or": {
            "name_sw": "ng'or",
            "name_en": "Ng'or / Luo traditional grain",
            "origin": "East Africa — traditional Luo grain, Homa Bay County",
            "status": "indigenous",
            "resilience_score": 0.85,
            "regions": ["Homa Bay", "Siaya", "Kisumu", "Migori", "Busia"],
            "traditional_uses": "Grain used in traditional porridge and ceremonial foods. Part of the Luo ritual grain triad (bel, kal, ng'or).",
            "nutrition": "High fibre, protein, iron. Comparable to finger millet in mineral density.",
            "gdd_base_temp": 12,
            "gdd_harvest": 1300,
            "temp_range": (18, 34),
            "precip_range": (2.0, 5.5),
            "soil_moisture_min": 0.15,
            "growing_days": 110,
            "water_need_mm": 350,
            "market_price_kes_tonne": 60000,
            "intercropping": ["finger_millet", "sorghum", "cowpea"],
            "market_demand": "Moderate for ceremonial use. Important for cultural food sovereignty.",
        },
        # ── Wild fruits (Ojwang, 2020 — Homa Bay County) ──
        "mapera": {
            "name_sw": "mapera",
            "name_en": "Mapera / Wild guava",
            "origin": "Naturalised in East Africa (Psidium guajava — introduced, now wild)",
            "status": "naturalised",
            "resilience_score": 0.75,
            "regions": ["Homa Bay", "Kisumu", "Siaya", "Migori", "Busia", "Vihiga", "Kakamega", "Kilifi", "Kwale"],
            "traditional_uses": "Fruit eaten fresh. Wild trees found along riverbanks and homesteads.",
            "nutrition": "Very high vitamin C (4x orange), dietary fibre, potassium, lycopene.",
            "gdd_base_temp": 15,
            "gdd_harvest": 2000,
            "temp_range": (18, 35),
            "precip_range": (2.0, 6.0),
            "soil_moisture_min": 0.15,
            "growing_days": 240,
            "water_need_mm": 600,
            "market_price_kes_tonne": 40000,
            "intercropping": [],
            "market_demand": "Moderate seasonal demand. Processed into juice and jam in some areas.",
        },
        "ochuoga": {
            "name_sw": "ochuoga",
            "name_en": "Ochuoga / Luo wild fruit",
            "origin": "East Africa — wild indigenous fruit, Lake Region",
            "status": "indigenous",
            "resilience_score": 0.72,
            "regions": ["Homa Bay", "Siaya", "Kisumu", "Migori", "Busia"],
            "traditional_uses": "Wild fruit eaten fresh. Harvested from bushes during fruiting season.",
            "nutrition": "Good source of vitamin C, natural sugars, and dietary fibre.",
            "gdd_base_temp": 18,
            "gdd_harvest": 1800,
            "temp_range": (20, 34),
            "precip_range": (2.5, 5.5),
            "soil_moisture_min": 0.2,
            "growing_days": 180,
            "water_need_mm": 400,
            "market_price_kes_tonne": 35000,
            "intercropping": [],
            "market_demand": "Limited commercialisation. Seasonal local consumption.",
        },
        "akuno": {
            "name_sw": "akuno",
            "name_en": "Akuno / Luo wild fruit",
            "origin": "East Africa — wild indigenous fruit",
            "status": "indigenous",
            "resilience_score": 0.78,
            "regions": ["Homa Bay", "Kisumu", "Siaya", "Migori", "Baringo", "Laikipia"],
            "traditional_uses": "Wild-harvested fruit, often consumed by children while herding. Dried for storage.",
            "nutrition": "Rich in vitamin C and antioxidants. Used traditionally for nutrition during food scarcity.",
            "gdd_base_temp": 18,
            "gdd_harvest": 2000,
            "temp_range": (20, 36),
            "precip_range": (2.0, 5.0),
            "soil_moisture_min": 0.1,
            "growing_days": 200,
            "water_need_mm": 350,
            "market_price_kes_tonne": 30000,
            "intercropping": [],
            "market_demand": "Very limited commercialisation. Valued as famine food and wild snack.",
        },
        "sangla": {
            "name_sw": "sangla",
            "name_en": "Sangla / Luo wild fruit",
            "origin": "East Africa — wild indigenous fruit",
            "status": "indigenous",
            "resilience_score": 0.70,
            "regions": ["Homa Bay", "Siaya", "Kisumu", "Migori", "Busia"],
            "traditional_uses": "Small wild fruit eaten fresh. Birds and children are primary harvesters.",
            "nutrition": "Source of natural sugars, vitamin C, and trace minerals.",
            "gdd_base_temp": 18,
            "gdd_harvest": 1600,
            "temp_range": (20, 34),
            "precip_range": (2.5, 5.5),
            "soil_moisture_min": 0.2,
            "growing_days": 150,
            "water_need_mm": 350,
            "market_price_kes_tonne": 28000,
            "intercropping": [],
            "market_demand": "Negligible commercial market. Subsistence and cultural value.",
        },
        "nyatonglo": {
            "name_sw": "nyatonglo",
            "name_en": "Nyatonglo / Luo wild fruit",
            "origin": "East Africa — wild indigenous fruit",
            "status": "indigenous",
            "resilience_score": 0.72,
            "regions": ["Homa Bay", "Kisumu", "Siaya", "Migori", "Kakamega"],
            "traditional_uses": "Wild berry harvested from shrubs. Eaten fresh in season.",
            "nutrition": "Contains vitamin C, flavonoids, and natural sugars.",
            "gdd_base_temp": 16,
            "gdd_harvest": 1500,
            "temp_range": (18, 32),
            "precip_range": (2.5, 6.0),
            "soil_moisture_min": 0.2,
            "growing_days": 150,
            "water_need_mm": 350,
            "market_price_kes_tonne": 32000,
            "intercropping": [],
            "market_demand": "Local subsistence consumption. Minimal market presence.",
        },
        "slenderleaf": {
            "name_sw": "mitoo/marejea",
            "name_en": "Slenderleaf / Mitoo",
            "origin": "East Africa (Crotalaria brevidens, C. ochroleuca)",
            "status": "indigenous",
            "resilience_score": 0.82,
            "regions": ["Siaya", "Kisumu", "Kakamega", "Bungoma", "Vihiga", "Homa Bay", "Busia"],
            "traditional_uses": "Intensely bitter leafy vegetable. Boiled, bitter water discarded, then mixed with milk, groundnut paste, or other vegetables. Valued in traditional medicine for gastrointestinal ailments.",
            "nutrition": "Extraordinary iron concentration (991mg/kg DW), calcium (718mg/kg), phosphorus (2375mg/kg). Highest iron of all indigenous vegetables.",
            "gdd_base_temp": 15,
            "gdd_harvest": 650,
            "temp_range": (16, 30),
            "precip_range": (2.5, 6.0),
            "soil_moisture_min": 0.2,
            "growing_days": 60,
            "water_need_mm": 250,
            "market_price_kes_tonne": 50000,
            "intercropping": ["jute_mallow", "sorghum", "cassava", "maize"],
            "market_demand": "Moderate but highly valued by Luo and Luhya communities. Premium price for pre-cooked packs in Nairobi.",
        },
        "desert_date": {
            "name_sw": "mchunju/mulului",
            "name_en": "Desert Date / Balanites",
            "origin": "East Africa — indigenous to arid savanna (Balanites aegyptiaca)",
            "status": "indigenous",
            "resilience_score": 0.98,
            "regions": ["Turkana", "Marsabit", "Garissa", "Kitui", "Baringo", "West Pokot"],
            "traditional_uses": "Fruit pulp eaten fresh or dried. Kernel yields high-quality edible oil for cooking and medicinal applications. Leaves are critical fodder during extreme drought.",
            "nutrition": "High energy density, rich in vitamin C, iron, and essential fatty acids.",
            "gdd_base_temp": 20,
            "gdd_harvest": 3650,
            "temp_range": (24, 42),
            "precip_range": (0.5, 3.0),
            "soil_moisture_min": 0.05,
            "growing_days": 365,
            "water_need_mm": 300,
            "market_price_kes_tonne": 120000,
            "intercropping": [],
            "market_demand": "Limited commercialisation. Critical famine food in ASALs. Growing superfood export potential.",
        },
        "bird_plum": {
            "name_sw": "mkuni/ekalale",
            "name_en": "Bird Plum / Brown Ivory",
            "origin": "East Africa — indigenous (Berchemia discolor)",
            "status": "indigenous",
            "resilience_score": 0.96,
            "regions": ["Turkana", "West Pokot", "Baringo", "Kitui", "Makueni"],
            "traditional_uses": "Small sweet yellow-brown fruits consumed fresh or dried for long-term storage. Crucial famine food in pastoralist communities.",
            "nutrition": "Very high sugar content, vitamin C, calcium.",
            "gdd_base_temp": 20,
            "gdd_harvest": 3650,
            "temp_range": (22, 40),
            "precip_range": (0.5, 3.0),
            "soil_moisture_min": 0.05,
            "growing_days": 365,
            "water_need_mm": 300,
            "market_price_kes_tonne": 90000,
            "intercropping": [],
            "market_demand": "Subsistence consumption in ASALs. Minimal market presence.",
        },
        "vitex_black_plum": {
            "name_sw": "mfudu/jwelu",
            "name_en": "Black Plum / Mfudu / Jwelu",
            "origin": "East Africa — indigenous (Vitex doniana)",
            "status": "indigenous",
            "resilience_score": 0.86,
            "regions": ["Homa Bay", "Kisumu", "Siaya", "Kakamega", "Kilifi", "Kwale", "Bungoma"],
            "traditional_uses": "Sweet plum-like black fruit consumed fresh or processed into jams and fermented beverages. Young leaves occasionally boiled as vegetable.",
            "nutrition": "Rich in simple carbohydrates, vitamin A, vitamin C.",
            "gdd_base_temp": 18,
            "gdd_harvest": 2000,
            "temp_range": (20, 34),
            "precip_range": (2.0, 5.5),
            "soil_moisture_min": 0.15,
            "growing_days": 240,
            "water_need_mm": 600,
            "market_price_kes_tonne": 50000,
            "intercropping": ["cassava", "maize", "banana"],
            "market_demand": "Moderate local demand. Processed jam has premium potential.",
        },
        "kale": {
            "name_sw": "sukuma wiki",
            "name_en": "Kale / Collard greens",
            "origin": "Mediterranean / Europe — colonial introduction",
            "status": "exotic",
            "resilience_score": 0.35,
            "regions": ["Kiambu", "Murang'a", "Nyeri", "Nakuru", "Uasin Gishu", "Trans Nzoia"],
            "traditional_uses": "Chopped and sauteed with tomatoes and onions.",
            "nutrition": "High vitamin K, vitamin C, calcium. Lower iron than indigenous vegetables.",
            "gdd_base_temp": 5,
            "gdd_harvest": 700,
            "temp_range": (12, 25),
            "precip_range": (3.0, 7.0),
            "soil_moisture_min": 0.3,
            "growing_days": 60,
            "water_need_mm": 300,
            "market_price_kes_tonne": 30000,
            "intercropping": ["maize", "beans"],
            "market_demand": "Most consumed leafy vegetable. Higher input requirements than indigenous alternatives.",
        },
        "cabbage": {
            "name_sw": "kabichi",
            "name_en": "Cabbage",
            "origin": "Europe / Mediterranean — colonial introduction",
            "status": "exotic",
            "resilience_score": 0.30,
            "regions": ["Kiambu", "Murang'a", "Nyeri", "Nakuru", "Uasin Gishu", "Trans Nzoia", "Narok"],
            "traditional_uses": "Sliced and cooked or used in coleslaw.",
            "nutrition": "High vitamin K, vitamin C, fibre. Lower nutritional density than indigenous vegetables.",
            "gdd_base_temp": 5,
            "gdd_harvest": 800,
            "temp_range": (12, 24),
            "precip_range": (3.0, 6.5),
            "soil_moisture_min": 0.35,
            "growing_days": 90,
            "water_need_mm": 350,
            "market_price_kes_tonne": 25000,
            "intercropping": ["maize", "beans"],
            "market_demand": "Very high in urban markets. High water/input requirements.",
        },
    }

    NUTRITION_MINERALS = {
        "slenderleaf": {"Fe": 991.0, "Ca": 718.0, "P": 2375.0, "K": 3296.0, "Mg": 822.0, "Na": 45.0},
        "black_nightshade": {"Fe": 450.5, "Ca": 3491.0, "P": 1833.0, "K": 4022.0, "Mg": 1140.0, "Na": 52.5},
        "spider_plant": {"Fe": 180.2, "Ca": 3477.0, "P": 3875.0, "K": 4549.0, "Mg": 747.0, "Na": 246.7},
        "jute_mallow": {"Fe": 225.2, "Ca": 2974.0, "P": 833.0, "K": 4098.0, "Mg": 1200.0, "Na": 101.8},
        "amaranth": {"Fe": 120.0, "Ca": 2150.0, "P": 1500.0, "K": 3500.0, "Mg": 800.0, "Na": 80.0},
        "cowpea_leaves": {"Fe": 180.0, "Ca": 1800.0, "P": 1200.0, "K": 3200.0, "Mg": 600.0, "Na": 60.0},
        "pumpkin_leaves": {"Fe": 150.0, "Ca": 2500.0, "P": 1000.0, "K": 3000.0, "Mg": 700.0, "Na": 90.0},
    }

    INTERCROPPING_ROW_RATIOS = {
        "sorghum_cowpea": {"ratio": "1:1 (alternating rows)", "source": "Empirical trials show sorghum yield increases 41.8% vs pure stand"},
        "finger_millet_pigeonpea": {"ratio": "2:1 (two rows millet : one row pigeonpea)", "mechanism": "Hydraulic lift — pigeonpea taproots draw water upward at night, releasing into upper soil profile for shallow-rooted millet"},
        "pigeonpea_cotton": {"ratio": "1:6 (one row pigeonpea : six rows cotton)", "source": "Minimises competition while providing fallback food supply if cotton prices crash"},
        "sorghum_soybean": {"ratio": "2:1 (two rows sorghum : one row soybean)", "mechanism": "Soybean fixes nitrogen; residual effect boosts subsequent sorghum"},
    }

    INTERCROPPING_PATTERNS = {
        "traditional_lake_region": {
            "name": "Lake Region polyculture (Luo/Luhya)",
            "counties": ["Kisumu", "Homa Bay", "Siaya", "Migori", "Busia", "Vihiga", "Kakamega", "Bungoma"],
            "crops": ["maize", "beans", "cassava", "black_nightshade", "spider_plant", "jute_mallow", "cowpea_leaves", "pumpkin_leaves", "sweet_potato"],
            "biodiversity_score": 0.85,
            "resilience_rating": "high",
        },
        "ukambani_dryland": {
            "name": "Ukambani dryland system (Kamba)",
            "counties": ["Machakos", "Kitui", "Makueni"],
            "crops": ["sorghum", "cowpea_leaves", "pigeon_pea", "cassava", "amaranth", "bambara_nut"],
            "biodiversity_score": 0.75,
            "resilience_rating": "very_high",
            "description": "Sorghum-cowpea intercropping boosts sorghum yield by 41.8% vs pure stand. Pigeonpea's deep taproot performs hydraulic lift, releasing moisture at night for shallow-rooted companions.",
        },
        "coastal_mixed": {
            "name": "Coast mixed system (Mijikenda)",
            "counties": ["Kilifi", "Kwale", "Taita Taveta", "Mombasa", "Lamu"],
            "crops": ["cassava", "cowpea_leaves", "sweet_potato", "pigeon_pea", "amaranth", "bambara_nut", "tamarind", "baobab"],
            "biodiversity_score": 0.9,
            "resilience_rating": "very_high",
        },
        "highland_kikuyu": {
            "name": "Central highlands system (Agikuyu/Embu/Meru)",
            "counties": ["Kiambu", "Murang'a", "Nyeri", "Meru", "Embu", "Tharaka Nithi"],
            "crops": ["maize", "beans", "black_nightshade", "amaranth", "sweet_potato", "pumpkin_leaves"],
            "biodiversity_score": 0.7,
            "resilience_rating": "moderate",
        },
        "luo_ritual_triad": {
            "name": "Luo ritual grain triad (bel+kal+ng'or)",
            "counties": ["Homa Bay", "Siaya", "Kisumu", "Migori", "Busia"],
            "crops": ["finger_millet", "sorghum", "ng_or"],
            "biodiversity_score": 0.65,
            "resilience_rating": "very_high",
            "cultural_significance": "The three grains (bel=finger millet, kal=sorghum, ng'or=a traditional grain) "
                "form a ritual triad used in Luo ceremonies including gwelruok (first fruits). "
                "Grown together in traditional systems for food security and cultural continuity.",
        },
        "maize_beans_pumpkin_three_sisters": {
            "name": "Maize-Bean-Pumpkin Three Sisters",
            "counties": ["Kiambu", "Murang'a", "Kakamega", "Bungoma", "Meru", "Embu"],
            "crops": ["maize", "beans", "pumpkin_leaves"],
            "biodiversity_score": 0.88,
            "resilience_rating": "high",
            "description": "Maize provides trellis for climbing beans. Beans fix nitrogen. Pumpkin vines form living mulch suppressing weeds and reducing evaporation.",
        },
        "pearl_millet_green_gram": {
            "name": "Pearl Millet + Green Gram (Tharaka/ASAL)",
            "counties": ["Tharaka Nithi", "Kitui", "Makueni", "Meru"],
            "crops": ["sorghum", "cowpea_leaves"],
            "biodiversity_score": 0.72,
            "resilience_rating": "very_high",
            "description": "Both crops possess extreme drought tolerance and rapid cycles. Green gram provides early harvest and nitrogen before millet canopy closes. Recommended row ratio: 1:1 alternating rows.",
        },
        "sorghum_soybean": {
            "name": "Sorghum + Soybean (Nyanza/Rift transition)",
            "counties": ["Narok", "Kisumu", "Homa Bay", "Migori"],
            "crops": ["sorghum", "cowpea_leaves"],
            "biodiversity_score": 0.75,
            "resilience_rating": "high",
            "description": "Soybean provides high-grade protein and nitrogen fixation. Residual nitrogen boosts subsequent sorghum yields. Recommended row ratio: 2:1 (sorghum:soybean).",
        },
        "banana_coffee_agroforestry": {
            "name": "Banana + Coffee + Agroforestry (Central Highlands)",
            "counties": ["Nyeri", "Kirinyaga", "Meru", "Embu", "Murang'a"],
            "crops": ["banana", "black_nightshade", "amaranth", "sweet_potato"],
            "biodiversity_score": 0.9,
            "resilience_rating": "high",
            "description": "Multi-tiered system. Tall trees provide shade, bananas provide mid-level canopy and mulch, coffee is cash crop understory. Shade-tolerant traditional vegetables on margins.",
        },
        "maize_groundnut": {
            "name": "Maize + Groundnut (Western Kenya / cross-border Tanzania)",
            "counties": ["Bungoma", "Busia", "Kakamega", "Migori"],
            "crops": ["maize", "cowpea_leaves"],
            "biodiversity_score": 0.78,
            "resilience_rating": "high",
            "description": "Groundnut provides high-value protein and oil. As a low-lying legume, it fixes nitrogen and provides ground cover without competing with maize canopy height. Increases protein yield per hectare vs maize monoculture.",
        },
        "pigeonpea_cotton_marginal_vertisol": {
            "name": "Pigeon Pea + Cotton (Marginal Vertisols / Lower Eastern)",
            "counties": ["Kitui", "Machakos", "Makueni", "Taita Taveta"],
            "crops": ["pigeon_pea", "sorghum"],
            "biodiversity_score": 0.68,
            "resilience_rating": "high",
            "description": "Cotton serves as primary cash crop, pigeonpea as insurance food crop. Deep roots break up heavy clay hardpans. Standard row ratio 1:6 (pigeonpea:cotton) minimises competition while providing fallback food supply if cotton prices crash.",
        },
        "agroforestry_legume_trees_maize_beans": {
            "name": "Agroforestry Legume Trees + Maize + Beans (Rift Valley)",
            "counties": ["Nakuru", "Baringo", "Laikipia", "Nandi", "Kericho"],
            "crops": ["maize", "beans", "sorghum"],
            "biodiversity_score": 0.82,
            "resilience_rating": "high",
            "description": "Nitrogen-fixing trees (Leucaena, Acacia) planted in alleys. Tree prunings used as green manure, increasing soil organic carbon and moisture retention.",
        },
    }

    FOOD_CORRIDORS = {
        "kisumu_nairobi": {
            "name": "Kisumu-Nairobi Corridor (Luo)",
            "origin_cities": ["Kisumu", "Siaya", "Homa Bay", "Migori"],
            "destination": "Nairobi (Kawangware, Kibera, Lang'ata, Eastlands)",
            "key_crops": ["black_nightshade", "spider_plant", "jute_mallow", "amaranth", "cassava", "sweet_potato"],
            "demand_intensity": "very_high",
            "food_remittance_context": "Over 50% of Nairobi households receive uncounted food remittances along this corridor from rural relatives",
        },
        "western_nairobi": {
            "name": "Western-Nairobi Corridor (Luhya)",
            "origin_cities": ["Busia", "Kakamega", "Bungoma", "Vihiga"],
            "destination": "Nairobi (Kawangware, Kangemi, Dagoretti)",
            "key_crops": ["spider_plant", "black_nightshade", "jute_mallow", "cassava", "yam", "sweet_potato"],
            "demand_intensity": "high",
        },
        "ukambani_nairobi": {
            "name": "Ukambani-Nairobi Corridor (Kamba)",
            "origin_cities": ["Machakos", "Kitui", "Makueni"],
            "destination": "Nairobi (Makadara, Eastlands, Mathare)",
            "key_crops": ["cowpea_leaves", "pigeon_pea", "amaranth", "cassava", "sorghum"],
            "demand_intensity": "high",
        },
        "central_nairobi": {
            "name": "Central Highlands-Nairobi (Agikuyu/Embu/Meru)",
            "origin_cities": ["Kiambu", "Murang'a", "Nyeri", "Meru", "Embu"],
            "destination": "Nairobi (All areas)",
            "key_crops": ["black_nightshade", "amaranth", "sweet_potato", "banana"],
            "demand_intensity": "very_high",
            "transition_context": "Severe early-2026 droughts caused near-total maize failures in Central Kenya. Farmers pivoting to hardy indigenous crops (amaranth, nightshade) with rapid maturation and lower irrigation requirements.",
        },
        "lake_region_nairobi_otc": {
            "name": "Lake Region-Nairobi OTC Bus Corridor",
            "origin_cities": ["Homa Bay", "Kisumu", "Siaya", "Migori", "Busia"],
            "destination": "Nairobi (Kawangware, Kibera, Lang'ata, Eastlands)",
            "key_crops": ["dek", "mito", "boo", "atipa", "odielo", "ndemra", "alikra",
                "black_nightshade", "spider_plant", "jute_mallow"],
            "demand_intensity": "high",
            "transport": "OTC buses and matatus carry fresh traditional vegetables overnight "
                "from Lake Region counties to Nairobi markets (Ojwang, 2020). Women farmers "
                "travel with produce, selling in Kawangware and Kibera by morning.",
        },
        "turkana_regional": {
            "name": "Turkana & ASALs to Regional Towns",
            "origin_cities": ["Lodwar", "Kakuma", "Lokichoggio", "Marsabit"],
            "destination": "Lodwar, Kitale, Nakuru",
            "key_crops": ["desert_date", "bird_plum", "sorghum", "cowpea_leaves"],
            "demand_intensity": "moderate",
            "transport": "Pastoralist networks and truck routes carry drought-famine foods from deep rural zones into regional trading towns, stabilizing food availability during peak drought.",
        },
        "busia_uganda_corridor": {
            "name": "Busia Corridor (Kenya-Uganda cross-border)",
            "origin_cities": ["Busia", "Tororo", "Mbale", "Jinja"],
            "destination": "Busia, Kisumu, Nairobi",
            "key_crops": ["amaranth", "cassava", "sweet_potato", "beans", "spider_plant"],
            "demand_intensity": "high",
            "transport": "Women Small-Scale Cross-Border Traders (WICBTs) dominate this route. Pineapples, cereals, legumes and vegetables move from Uganda's eastern regions into Western Kenya and onward to Nairobi. Despite the Simplified Trade Regime (STR), WICBTs face non-tariff barriers, extortion by border officials, and bureaucratic bottlenecks at the One Stop Border Post. Many are forced to use informal ungazetted crossing points (panya routes), expediting transit but exposing them to harassment, violence, and goods confiscation.",
        },
        "ukambani_mombasa": {
            "name": "Ukambani-Mombasa Corridor (Kamba)",
            "origin_cities": ["Machakos", "Kitui", "Makueni"],
            "destination": "Mombasa (coastal urban and tourism populations)",
            "key_crops": ["cowpea_leaves", "pigeon_pea", "amaranth", "baobab", "tamarind", "sorghum"],
            "demand_intensity": "high",
            "transport": "Non-perishable drought-tolerant pulses (cowpeas, green grams, pigeonpeas) and dryland fruits (baobab, tamarind) transported by highway to Mombasa. Critical protein supply for coastal communities.",
        },
        "namanga_tanzania_corridor": {
            "name": "Namanga Corridor (Kenya-Tanzania cross-border)",
            "origin_cities": ["Arusha", "Moshi", "Namanga"],
            "destination": "Namanga, Nairobi, Mombasa",
            "key_crops": ["sorghum", "cowpea_leaves", "pigeon_pea", "beans", "amaranth"],
            "demand_intensity": "high",
            "transport": "Women Small-Scale Cross-Border Traders (WICBTs) move grains, legumes and livestock from Tanzania's northern agricultural zones into Kenya. Despite the Simplified Trade Regime designed to facilitate tariff-free movement, women face systemic barriers and are often forced onto panya routes (informal crossings) to avoid rapid spoilage of perishable cargo.",
        },
    }

    def __init__(self):
        self._by_name = {}
        self._by_region = {}
        self._by_status = {}
        for key, info in self.CROP_INDEX.items():
            self._by_name[key] = info
            self._by_name[info["name_sw"].split("/")[0].strip()] = info
            self._by_name[info["name_en"].lower()] = info
            for region in info.get("regions", []):
                self._by_region.setdefault(region.upper(), []).append(info)
            status = info.get("status", "unknown")
            self._by_status.setdefault(status, []).append(info)

    def classify_crop(self, crop_name: str) -> CropClassification | None:
        crop_name = crop_name.lower().strip()
        if crop_name in self._by_name:
            return self._by_name[crop_name] | {"key": crop_name}
        for key, info in self.CROP_INDEX.items():
            if crop_name in info.get("name_en", "").lower() or crop_name in info.get("name_sw", "").lower():
                return info | {"key": key}
        return None

    def list_by_status(self, status: str) -> list[dict]:
        return self._by_status.get(status, [])

    def list_indigenous(self) -> list[dict]:
        return self._by_status.get("indigenous", [])

    def list_naturalised(self) -> list[dict]:
        return self._by_status.get("naturalised", [])

    def list_exotic(self) -> list[dict]:
        return self._by_status.get("exotic", [])

    def list_all(self) -> list[dict]:
        return [info | {"key": key} for key, info in self.CROP_INDEX.items()]

    def get_crops_for_region(self, county: str) -> list[dict]:
        return self._by_region.get(county.upper(), [])

    def get_intercropping_patterns(self, county: str | None = None) -> list[dict]:
        if county is None:
            return list(self.INTERCROPPING_PATTERNS.values())
        county = county.upper()
        return [p for p in self.INTERCROPPING_PATTERNS.values()
                if any(c.upper() == county for c in p["counties"])]

    def get_food_corridors(self, county: str | None = None) -> list[dict]:
        if county is None:
            return list(self.FOOD_CORRIDORS.values())
        county = county.upper()
        return [c for c in self.FOOD_CORRIDORS.values()
                if county in [o.upper() for o in c["origin_cities"]]]

    def get_nutritional_context(self, crop_name: str) -> dict:
        info = self.classify_crop(crop_name)
        if not info:
            return {}
        return {
            "crop": crop_name,
            "nutrition": info.get("nutrition", ""),
            "status": info.get("status", ""),
            "value_proposition": (
                "Indigenous crop — naturally adapted to local conditions, "
                "often higher nutritional density than exotic alternatives"
                if info.get("status") == "indigenous"
                else "Naturalised crop — well-adapted, complementary to indigenous varieties"
                if info.get("status") == "naturalised"
                else "Exotic crop — requires higher inputs, important for market access"
            ),
        }

    def get_nutrition_minerals(self, crop_name: str) -> dict:
        info = self.classify_crop(crop_name)
        if not info:
            return {}
        index_key = info.get("key", crop_name)
        if index_key not in self.CROP_INDEX:
            for k in self.CROP_INDEX:
                sw = self.CROP_INDEX[k].get("name_sw", "")
                en = self.CROP_INDEX[k].get("name_en", "").lower()
                if index_key == k or index_key in sw or index_key in en:
                    index_key = k
                    break
        minerals = self.NUTRITION_MINERALS.get(index_key, {})
        return {
            "crop": crop_name,
            "status": info.get("status", ""),
            "mineral_composition_mg_per_kg_dw": minerals,
            "iron_rich": minerals.get("Fe", 0) > 300,
            "calcium_rich": minerals.get("Ca", 0) > 2000,
            "note": (
                "Pharmaceutical-grade iron density — critical for anemia intervention"
                if minerals.get("Fe", 0) > 500
                else "Good mineral source"
            ) if minerals else "Mineral data not available",
        }

    def get_resilience_rating(self, crops: list[str]) -> dict:
        indigenous_factor = sum(1 for c in crops if self.classify_crop(c) and self.classify_crop(c).get("status") in ("indigenous", "naturalised"))
        total = len(crops) or 1
        indigenous_ratio = indigenous_factor / total
        return {
            "indigenous_crop_ratio": round(indigenous_ratio, 2),
            "resilience_score": round(0.3 + 0.7 * indigenous_ratio, 2),
            "note": (
                "Higher ratio of indigenous crops indicates better climate adaptation"
                if indigenous_ratio > 0.5
                else "Predominantly exotic crops — higher input dependency"
            ),
        }
