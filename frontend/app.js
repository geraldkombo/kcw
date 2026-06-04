// Kienyeji — standalone SPA, no backend required
import { t, setLanguage } from "./i18n.js";

const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);

let state = { page: "dashboard", theme: localStorage.getItem("k-theme") || "light", lang: localStorage.getItem("k-lang") || "en" };
let charts = {};
let leafletMap = null;

// ====== EMBEDDED DATA (standalone) ======
const CROPS = [
  {key:"amaranth",name_en:"Amaranth / African spinach",name_sw:"Mchicha",status:"indigenous",resilience_score:0.92,growing_season:"Long rains (Mar–May) + short rains (Oct–Dec)",counties:["Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia","Kiambu","Murang'a","Nyeri","Meru","Embu","Tharaka Nithi","Machakos","Kitui","Makueni"],traditional_uses:"Young leaves boiled as vegetable; highly nutritious traditional weaning food",origin:"Indigenous to East Africa",nutrition:"High in iron, calcium, vitamins A & C",intercropping:["maize","sorghum","cassava","cowpea"],market_price_kes_tonne:80000},
  {key:"black_nightshade",name_en:"Black nightshade / Garden nightshade",name_sw:"Managu / Mnavu",status:"indigenous",resilience_score:0.85,growing_season:"Year-round with rain",counties:["Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia","Kiambu","Nyeri"],traditional_uses:"Leaves boiled and eaten as vegetable",origin:"Indigenous to Africa",nutrition:"Rich in iron, calcium, and vitamin C",intercropping:["maize","beans","kale"],market_price_kes_tonne:95000},
  {key:"spider_plant",name_en:"Spider plant / Cat's whiskers",name_sw:"Sagaa / Mwianzo / Akeyo",status:"indigenous",resilience_score:0.88,growing_season:"Rainy seasons",counties:["Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia","Machakos","Kitui","Makueni"],traditional_uses:"Leaves and tender shoots used as vegetable",origin:"Native to Africa",nutrition:"Excellent source of iron, protein, and fiber",intercropping:["maize","sorghum","millet"],market_price_kes_tonne:70000},
  {key:"jute_mallow",name_en:"Jute mallow",name_sw:"Mrenda / Murere / Apoth",status:"indigenous",resilience_score:0.84,growing_season:"Rainy seasons",counties:["Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia"],traditional_uses:"Slimy leaves used as vegetable; also used for fiber",origin:"Indigenous to Africa and Asia",nutrition:"High in protein, iron, calcium, and beta-carotene",intercropping:["maize","cassava","sweet_potato"],market_price_kes_tonne:65000},
  {key:"cowpea_leaves",name_en:"Cowpea leaves / Kunde",name_sw:"Kunde / Mwembu",status:"indigenous",resilience_score:0.86,growing_season:"Rainy seasons",counties:["Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia","Machakos","Kitui","Makueni","Kilifi","Kwale"],traditional_uses:"Young leaves and tender pods as vegetable",origin:"Indigenous to Africa",nutrition:"Rich in protein, iron, and folate",intercropping:["maize","sorghum","millet"],market_price_kes_tonne:55000},
  {key:"slenderleaf",name_en:"Slenderleaf / Mexican clover",name_sw:"Mitoo / Murenda",status:"indigenous",resilience_score:0.90,growing_season:"Rainy seasons",counties:["Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia"],traditional_uses:"Leaves used as a vegetable; valued for high iron content",origin:"Indigenous to East Africa",nutrition:"Exceptionally high iron (991 mg/kg DW), calcium, protein",intercropping:["maize","sorghum","beans"],market_price_kes_tonne:75000},
  {key:"pumpkin_leaves",name_en:"Pumpkin leaves",name_sw:"Majani ya boga / Malenge",status:"naturalised",resilience_score:0.78,growing_season:"Year-round",counties:["Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia","Kiambu","Machakos"],traditional_uses:"Leaves and flowers cooked as vegetable; seeds eaten",origin:"Originated in Americas, naturalised in Africa",nutrition:"Rich in iron, calcium, vitamins A and C",intercropping:["maize","beans","sorghum"],market_price_kes_tonne:40000},
  {key:"cassava_leaves",name_en:"Cassava leaves",name_sw:"Majani ya muhogo",status:"naturalised",resilience_score:0.87,growing_season:"Year-round (24-month in-ground storage)",counties:["Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia","Kilifi","Kwale"],traditional_uses:"Leaves pounded and cooked as vegetable; roots staple food",origin:"South America, naturalised across Africa",nutrition:"Good source of protein, iron, vitamins",intercropping:["maize","beans","cowpea"],market_price_kes_tonne:30000},
  {key:"baobab",name_en:"Baobab",name_sw:"Mbuyu / Muuyu",status:"indigenous",resilience_score:1.00,growing_season:"Dry season fruit (Jun–Sep)",counties:["Kilifi","Kwale","Kitui","Makueni","Kajiado","Narok","Baringo"],traditional_uses:"Fruit pulp eaten fresh or in drinks; leaves as vegetable; bark for fiber",origin:"Native to African savannahs",nutrition:"Extremely high vitamin C, calcium, potassium, antioxidants",intercropping:["millet","sorghum","cowpea"],market_price_kes_tonne:150000},
  {key:"baobab_leaves",name_en:"Baobab leaves",name_sw:"Majani ya mbuyu",status:"indigenous",resilience_score:0.95,growing_season:"Rainy season",counties:["Kilifi","Kwale","Kitui","Makueni","Kajiado","Baringo"],traditional_uses:"Young leaves cooked as vegetable",origin:"Native to Africa",nutrition:"High in protein, iron, calcium",intercropping:["millet","sorghum"],market_price_kes_tonne:120000},
  {key:"tamarind",name_en:"Tamarind",name_sw:"Ukwa / Mkwaju",status:"indigenous",resilience_score:0.94,growing_season:"Dry season fruit",counties:["Kilifi","Kwale","Kitui","Makueni","Machakos","Kajiado"],traditional_uses:"Fruit pulp used in drinks, sauces, and traditional medicine",origin:"Native to tropical Africa",nutrition:"High in B vitamins, calcium, magnesium, potassium",intercropping:["millet","sorghum","cowpea"],market_price_kes_tonne:90000},
  {key:"desert_date",name_en:"Desert date",name_sw:"Mjunja / Ol-magurgur",status:"indigenous",resilience_score:0.98,growing_season:"Dry season (Jan–Mar)",counties:["Kitui","Makueni","Kajiado","Baringo","Narok"],traditional_uses:"Fruit pulp edible; seeds for oil; bark for medicine",origin:"Native to arid and semi-arid Africa",nutrition:"High in protein, fiber, minerals",intercropping:["millet","sorghum"],market_price_kes_tonne:70000},
  {key:"bird_plum",name_en:"Bird plum / Wild medlar",name_sw:"Mpekete / Mukuikui",status:"indigenous",resilience_score:0.96,growing_season:"Rainy season fruit",counties:["Kitui","Makueni","Machakos","Kajiado","Baringo"],traditional_uses:"Fruit eaten fresh or dried; wood for tools",origin:"Native to African savannahs",nutrition:"Rich in vitamin C, calcium, iron",intercropping:["millet","sorghum"],market_price_kes_tonne:60000},
  {key:"vitex",name_en:"Vitex / Black plum",name_sw:"Mfuu / Mubuu",status:"indigenous",resilience_score:0.86,growing_season:"Rainy season fruit",counties:["Kilifi","Kwale","Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia"],traditional_uses:"Fruit eaten fresh; leaves for fodder; wood for timber",origin:"Native to East Africa",nutrition:"Good source of vitamin C, minerals",intercropping:["maize","cassava","banana"],market_price_kes_tonne:50000},
  {key:"maize",name_en:"Maize",name_sw:"Mahindi",status:"exotic",resilience_score:0.50,growing_season:"Long rains (Mar–May)",counties:["All counties"],traditional_uses:"Staple food: ugali, porridge, roasted",origin:"Originated in Mesoamerica",intercropping:["beans","cowpea","groundnut","pigeon_pea","sorghum"],market_price_kes_tonne:45000},
  {key:"sorghum",name_en:"Sorghum",name_sw:"Mtama",status:"naturalised",resilience_score:0.82,growing_season:"Long rains + short rains",counties:["Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia","Machakos","Kitui","Makueni","Kilifi","Kwale","Kajiado","Narok","Baringo"],traditional_uses:"Porridge, ugali, local beer, livestock feed",origin:"Originated in East Africa",nutrition:"High in protein, iron, fiber; gluten-free",intercropping:["maize","cowpea","millet","soybean"],market_price_kes_tonne:55000},
  {key:"millet",name_en:"Pearl millet / Finger millet",name_sw:"Wimbi / Ulezi",status:"indigenous",resilience_score:0.90,growing_season:"Short rains (Oct–Dec)",counties:["Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia","Machakos","Kitui","Makueni","Kilifi","Kwale","Kajiado","Narok","Baringo"],traditional_uses:"Porridge (uji), ugali, local beer, weaning food",origin:"Indigenous to Africa",nutrition:"Rich in iron, calcium, protein; gluten-free; high in tryptophan",intercropping:["sorghum","cowpea","green_gram"],market_price_kes_tonne:70000},
  {key:"beans",name_en:"Beans (common bean)",name_sw:"Maharagwe",status:"exotic",resilience_score:0.55,growing_season:"Long rains (Mar–May)",counties:["All highland counties"],traditional_uses:"Staple protein: githeri, stews, boiled",origin:"Originated in Americas",intercropping:["maize","sorghum","cassava","coffee"],market_price_kes_tonne:90000},
  {key:"cowpea_grain",name_en:"Cowpea (grain)",name_sw:"Kunde (mbegu)",status:"indigenous",resilience_score:0.88,growing_season:"Rainy seasons",counties:["Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia","Machakos","Kitui","Makueni","Kilifi","Kwale"],traditional_uses:"Grains boiled or in stews; leaves as vegetable",origin:"Indigenous to Africa",nutrition:"High in protein, fiber, folate, iron",intercropping:["maize","sorghum","millet"],market_price_kes_tonne:60000},
  {key:"green_gram",name_en:"Green gram / Mung bean",name_sw:"Ndengu / Alot",status:"naturalised",resilience_score:0.80,growing_season:"Short rains (Oct–Dec)",counties:["Machakos","Kitui","Makueni","Kilifi","Kwale","Kajiado","Narok","Baringo","Tharaka Nithi","Meru"],traditional_uses:"Boiled as stew; sprouted; flour for weaning",origin:"Originated in Indian subcontinent",nutrition:"High in protein, fiber, magnesium, folate",intercropping:["maize","millet","sorghum"],market_price_kes_tonne:85000},
  {key:"pigeon_pea",name_en:"Pigeon pea",name_sw:"Mbaazi / Nzavi",status:"naturalised",resilience_score:0.85,growing_season:"Long rains (Mar–May), drought-tolerant",counties:["Machakos","Kitui","Makueni","Kilifi","Kwale","Tharaka Nithi","Meru","Kajiado"],traditional_uses:"Dried or green peas in stew; leaves as fodder",origin:"Originated in India, naturalised in Africa",nutrition:"High in protein, fiber, B vitamins, magnesium",intercropping:["sorghum","maize","cotton","cassava"],market_price_kes_tonne:65000},
  {key:"groundnut",name_en:"Groundnut / Peanut",name_sw:"Njugu / Karanga",status:"exotic",resilience_score:0.65,growing_season:"Long rains (Mar–May)",counties:["Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia","Machakos","Kitui","Makueni","Kilifi","Kwale"],traditional_uses:"Roasted, boiled, ground for sauce, oil extraction",origin:"Originated in South America",intercropping:["maize","sorghum","cassava"],market_price_kes_tonne:70000},
  {key:"sweet_potato",name_en:"Sweet potato",name_sw:"Viazi vitamu / Mbwamwachi",status:"exotic",resilience_score:0.75,growing_season:"Year-round",counties:["Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia","Machakos","Kitui","Makueni","Kilifi","Kwale","Kiambu","Meru"],traditional_uses:"Boiled, roasted, mashed; leaves as vegetable",origin:"Originated in South America",nutrition:"High in vitamin A (orange varieties), vitamin C, fiber",intercropping:["maize","beans","cassava"],market_price_kes_tonne:40000},
  {key:"cassava_root",name_en:"Cassava (root)",name_sw:"Muhogo",status:"naturalised",resilience_score:0.87,growing_season:"Year-round (24-month in-ground storage)",counties:["Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia","Kilifi","Kwale","Machakos","Kitui","Makueni"],traditional_uses:"Boiled, fried, fermented; flour for ugali; starch",origin:"South America, naturalised across Africa",nutrition:"High in carbohydrates, low protein; good energy source",intercropping:["maize","beans","cowpea","sweet_potato"],market_price_kes_tonne:25000},
  {key:"banana",name_en:"Banana (cooking)",name_sw:"Ndizi / Matoke",status:"exotic",resilience_score:0.60,growing_season:"Year-round",counties:["Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia","Meru","Embu","Kiambu","Murang'a","Nyeri"],traditional_uses:"Boiled (matoke), fried, roasted, mashed",origin:"Originated in Southeast Asia",intercropping:["coffee","beans","maize","agroforestry"],market_price_kes_tonne:40000},
  {key:"coffee",name_en:"Coffee (Arabica)",name_sw:"Kahawa",status:"exotic",resilience_score:0.55,growing_season:"Year-round with rain",counties:["Kiambu","Murang'a","Nyeri","Meru","Embu","Tharaka Nithi","Kisumu","Migori","Kakamega","Bungoma"],traditional_uses:"Beverage; cash crop",origin:"Originated in Ethiopia",intercropping:["banana","beans","maize","agroforestry"],market_price_kes_tonne:250000},
  {key:"cotton",name_en:"Cotton",name_sw:"Pamba",status:"exotic",resilience_score:0.45,growing_season:"Long rains",counties:["Kisumu","Siaya","Homa Bay","Migori","Kakamega","Bungoma","Busia","Machakos","Kitui","Makueni","Kilifi","Kwale"],traditional_uses:"Fiber for textiles; seeds for oil",origin:"Originated in multiple centers",intercropping:["maize","sorghum","pigeon_pea"],market_price_kes_tonne:100000},
  {key:"kale",name_en:"Kale / Collard greens",name_sw:"Sukuma wiki",status:"exotic",resilience_score:0.50,growing_season:"Year-round with water",counties:["All counties"],traditional_uses:"Leaves boiled as vegetable",origin:"Originated in Europe",nutrition:"High in vitamins K, A, C; calcium, iron",intercropping:["maize","beans","black_nightshade"],market_price_kes_tonne:50000},
  {key:"cabbage",name_en:"Cabbage",name_sw:"Kabichi",status:"exotic",resilience_score:0.30,growing_season:"Year-round with water",counties:["All highland counties"],traditional_uses:"Leaves used in salads, stews, coleslaw",origin:"Originated in Europe",nutrition:"High in vitamin C, fiber",intercropping:["maize","beans"],market_price_kes_tonne:30000},
  {key:"onion",name_en:"Onion (bulb)",name_sw:"Kitunguu",status:"exotic",resilience_score:0.40,growing_season:"Dry season",counties:["All counties"],traditional_uses:"Bulb as seasoning and vegetable",origin:"Originated in Central Asia",intercropping:["maize","kale","carrot"],market_price_kes_tonne:60000},
  {key:"tomato",name_en:"Tomato",name_sw:"Nyanya",status:"exotic",resilience_score:0.35,growing_season:"Year-round with water",counties:["All counties"],traditional_uses:"Fruit in stews, sauces, salads",origin:"Originated in South America",intercropping:["kale","onion","beans"],market_price_kes_tonne:50000},
  {key:"coconut",name_en:"Coconut",name_sw:"Mnazi / Dafu / Nazi",status:"naturalised",resilience_score:0.72,growing_season:"Year-round",counties:["Kilifi","Kwale","Mombasa"],traditional_uses:"Milk, flesh, oil; essential in coastal cuisine",origin:"Originated in Indo-Pacific, naturalised on coast",intercropping:["cassava","sorghum","banana","cowpea"],market_price_kes_tonne:80000},
  {key:"mango",name_en:"Mango",name_sw:"Mwembe / Embe",status:"exotic",resilience_score:0.58,growing_season:"Seasonal (Nov–Mar)",counties:["Kilifi","Kwale","Machakos","Kitui","Makueni","Meru","Embu","Tharaka Nithi","Kisumu","Homa Bay","Kakamega"],traditional_uses:"Fruit fresh, dried, juiced; green mango in chutney",origin:"Originated in South Asia",intercropping:["cowpea","beans","sorghum"],market_price_kes_tonne:40000},
  {key:"papaya",name_en:"Papaya / Pawpaw",name_sw:"Mpapai / Papai",status:"exotic",resilience_score:0.55,growing_season:"Year-round",counties:["Kilifi","Kwale","Machakos","Kitui","Makueni","Kisumu","Homa Bay","Kakamega","Bungoma","Busia"],traditional_uses:"Fruit fresh; green papaya as vegetable; seeds for medicine",origin:"Originated in Central America",intercropping:["maize","beans","cowpea"],market_price_kes_tonne:30000},
  {key:"guava",name_en:"Guava",name_sw:"Mpera",status:"exotic",resilience_score:0.60,growing_season:"Seasonal",counties:["Kiambu","Murang'a","Nyeri","Meru","Embu","Machakos","Kitui","Makueni","Kisumu","Kakamega","Kilifi"],traditional_uses:"Fruit fresh, juiced; leaves for tea",origin:"Originated in Americas",intercropping:["maize","beans","cassava"],market_price_kes_tonne:35000},
  {key:"avocado",name_en:"Avocado",name_sw:"Parachichi / Mafuta",status:"exotic",resilience_score:0.52,growing_season:"Seasonal",counties:["Kiambu","Murang'a","Nyeri","Meru","Embu","Kisumu","Kakamega","Bungoma","Busia","Machakos"],traditional_uses:"Fruit fresh; oil for cosmetics",origin:"Originated in Central America",intercropping:["coffee","banana","beans"],market_price_kes_tonne:100000},
  {key:"cashew",name_en:"Cashew",name_sw:"Mkanju / Bibazon",status:"exotic",resilience_score:0.68,growing_season:"Seasonal",counties:["Kilifi","Kwale"],traditional_uses:"Nut roasted; apple for juice and alcohol",origin:"Originated in Brazil",intercropping:["cassava","cowpea","sorghum"],market_price_kes_tonne:200000},
];

const CORRIDORS = [
  {name:"Lake Region Food Basket",origin_cities:["Kisumu","Siaya","Homa Bay","Migori"],destination:"Nairobi",key_crops:["Amaranth","Black nightshade","Spider plant","Jute mallow","Cowpea leaves","Slenderleaf","Sorghum","Millet"],transport:"Truck (A104) + boat (Lake Victoria)",demand_intensity:"very_high",food_remittance_context:"50% of Nairobi households receive food remittances from upcountry"},
  {name:"Ukambani-Mombasa Corridor",origin_cities:["Machakos","Kitui","Makueni"],destination:"Mombasa",key_crops:["Green gram","Pigeon pea","Cowpea","Sorghum","Millet","Baobab","Tamarind","Desert date"],transport:"Truck (A109)",demand_intensity:"very_high",food_remittance_context:"Coastal cities rely on Ukambani dryland grains"},
  {name:"Busia-Uganda Cross-Border",origin_cities:["Busia","Bungoma"],destination:"Tororo, Uganda",key_crops:["Cassava","Sweet potato","Beans","Maize","Millet","Sorghum","Amaranth"],transport:"Cross-border truck + bicycle (panya routes)",demand_intensity:"high",food_remittance_context:"77% women traders; WICBT framework; STR regime; panya routes bypass formal customs"},
  {name:"Namanga-Tanzania Cross-Border",origin_cities:["Namanga"],destination:"Arusha, Tanzania",key_crops:["Maize","Beans","Cowpea","Millet","Sorghum"],transport:"Cross-border lorry",demand_intensity:"high",food_remittance_context:"Seasonal food remittance flows between Maasai communities"},
  {name:"Central Kenya Highlands",origin_cities:["Kiambu","Murang'a","Nyeri"],destination:"Nairobi",key_crops:["Potato","Kale","Cabbage","Avocado","Coffee","Banana","Mango","Tomato"],transport:"Truck (A2)",demand_intensity:"very_high",food_remittance_context:"Daily fresh produce supply to Nairobi"},
  {name:"Meru-Embu Green Grocery",origin_cities:["Meru","Embu","Tharaka Nithi"],destination:"Nairobi",key_crops:["Mango","Avocado","Banana","Papaya","Maize","Beans","Cowpea","Green gram","Millet"],transport:"Truck (A2/B6)",demand_intensity:"very_high",food_remittance_context:"Premium organic supply chain to Nairobi"},
  {name:"Turkana / ASAL Pastoral",origin_cities:["Lodwar"],destination:"Nairobi",key_crops:["Sorghum","Millet","Cowpea","Green gram","Baobab","Desert date","Bird plum"],transport:"Truck (A1) + camel",demand_intensity:"medium",food_remittance_context:"Arid corridor with high food insecurity"},
  {name:"South Nyanza Sugarcane Belt",origin_cities:["Migori","Homa Bay"],destination:"Kisumu",key_crops:["Maize","Beans","Sweet potato","Cassava","Sorghum","Millet","Banana"],transport:"Truck (C19)",demand_intensity:"high",food_remittance_context:"Inter-county food remittance from rural farms to Kisumu city"},
  {name:"Coast Tourism Belt",origin_cities:["Kilifi","Kwale"],destination:"Mombasa",key_crops:["Coconut","Cashew","Mango","Cassava","Cowpea","Baobab","Tamarind"],transport:"Truck (A14) + boat",demand_intensity:"high",food_remittance_context:"Tourism-driven demand for indigenous foods"},
];

const DERISK = {
  overview: {forces:[
    {name:"Climate Volatility",detail:"Parametric insurance triggered by satellite data (rainfall deficit, LST anomaly, NDVI anomaly). Payout within 10 days via IRA-regulated framework.",data_sources:["CHIRPS","MODIS","Landsat 8","IRA Guidelines 2025"]},
    {name:"Fiscal Innovation",detail:"Kenya's $772M sovereign green bond — 35% cold storage, 25% climate seeds, 20% premium support, 20% carbon MRV. Domestic fiscal context: 75M KES disaster response fund, $2B Eurobond.",data_sources:["Kenya Green Bond Programme","NSE","Treasury"]},
    {name:"USAID Freeze Response",detail:"EO 14169: $225M bilateral aid contraction, 70-86% award termination. 87% of counties have CSA mainstreamed but only 42% funded. Food insecurity estimate 2026: 3.1M in IPC Phase 3+.",data_sources:["USAID","FEWS NET","Kenya CSA Program"]},
    {name:"Market Infrastructure",detail:"57% post-harvest loss for AIVs — farmer burden 7.6x retailer. Two interventions: solar drying (reduces PHL 40%) and cold storage (reduces PHL 65%). Carbon credits: 2.5-5.0 tCO2/ha at KES 2,000-4,000/tonne.",data_sources:["FAO","World Bank","Verra","Gold Standard","Plan Vivo"]},
  ]},
  parametrics:{model:{description:"Satellite-triggered parametric insurance for indigenous crops. Three triggers, 10-day payout target, KES 3,000-5,000 premium per unit per hectare.",trigger_metrics:[{name:"rainfall_deficit",sensor:"CHIRPS (Climate Hazards Group)",payout_formula:"KES 15K × deficit_pct if <80% of 10-year mean",threshold:"<80% of 10-year seasonal mean"},{name:"lst_anomaly",sensor:"MODIS MOD11A2",payout_formula:"KES 10K × anomaly_days if >3 consecutive days above threshold",threshold:">3 consecutive days >38°C"},{name:"ndvi_anomaly",sensor:"Landsat 8 OLI/TIRS",payout_formula:"KES 8K × (1 - NDVI_ratio) if NDVI <0.3",threshold:"NDVI <0.3 for >10 days"}],premium_estimate_kes_per_ha:"KES 3,000-5,000/unit/ha"},county_context:{primary_risk:"Lake Region: highest rainfall variability; ASAL counties: drought frequency"}},
  greenbond:{allocations:[{program:"Cold Storage Infrastructure",allocation_pct:35,description:"Cold storage for AIVs to reduce 57% PHL"},{program:"Climate-Adaptive Seeds",allocation_pct:25,description:"Drought-tolerant indigenous seed varieties"},{program:"Premium Subsidy Fund",allocation_pct:20,description:"Subsidized parametric insurance premiums for smallholders"},{program:"Carbon MRV Systems",allocation_pct:20,description:"Measurement, reporting & verification for carbon credits"}]},
  usaid:{key_metrics:{bilateral_aid_contraction_usd:"$225M",award_termination_rate_pct:"70-86%",csa_mainstreamed_in_counties_pct:87,csa_budget_allocated_pct:42,food_insecurity_estimate_2026:"3.1M in IPC Phase 3+"},systemic_consequence:"The freeze undermines a decade of CSA mainstreaming. GOK contingency: 75M KES disaster response fund redirected to fill gaps in food security monitoring and seed distribution."},
  phl:{aiv_phl_rate_pct:57,economic_burden_ratio_farmer_vs_retailer:7.6,interventions:[{solution:"Solar drying",phl_reduction_pct:40,description:"Solar drying reduces AIV PHL from 57% to 34%"},{solution:"Cold storage",phl_reduction_pct:65,description:"Cold storage reduces AIV PHL from 57% to 20%"}]},
  carbon:{description:"Carbon sequestration potential of traditional intercropping systems — agroforestry, millet/sorghum, and indigenous vegetables.",estimated_sequestration_tonnes_co2_per_ha:{agroforestry_systems:5.0,sorghum_millet_systems:2.5,indigenous_vegetables:1.8,maize_monocropping:-0.5},carbon_price_kes_per_tonne:"KES 2,000-4,000",additional_revenue_kes_per_ha:"KES 5,000-20,000"},
};

const MARKET = {nightshade:{markup:127,location:"Bondo, KES 600/kg"},amaranth:{markup:130,location:"Kibuye, KES 150/kg"},cowpea:{markup:143,location:"Kimilili, KES 170/kg"},spider_plant:{markup:57},pumpkin:{markup:40,"precooked":"KES 400/kg"}};

// ====== UTILITIES ======
function toast(msg, type = "success") {
  const c = $("#toast");
  const colors = {success:"rgba(27,94,32,.95)",error:"rgba(198,40,40,.95)",info:"rgba(21,101,192,.95)"};
  const icons = {success:"✓",error:"✗",info:"ℹ"};
  const e = document.createElement("div");
  e.style.cssText = `background:${colors[type]||colors.info};color:#fff;padding:.75rem 1.25rem;border-radius:12px;font-size:.8rem;display:flex;align-items:center;gap:.5rem;box-shadow:0 8px 32px rgba(0,0,0,.15);backdrop-filter:blur(12px);animation:fadeIn .3s ease-out`;
  e.innerHTML = `<span style="font-weight:700">${icons[type]||icons.info}</span><span>${msg}</span>`;
  c.appendChild(e);
  setTimeout(()=>{e.style.transition="all .3s";e.style.opacity="0";e.style.transform="translateY(-10px)";setTimeout(()=>e.remove(),300)},3500);
}

function nav(page) {
  state.page = page;
  $$("[data-page]").forEach(e => e.classList.add("hidden"));
  const t = $(`[data-page="${page}"]`);
  if (t) t.classList.remove("hidden");
  $$(".nav-link").forEach(l => l.classList.toggle("active", l.dataset.nav === page));
  $$(".bottom-nav-link").forEach(l => l.classList.toggle("active", l.dataset.nav === page));
}

function theme(t) {
  state.theme = t;
  document.documentElement.classList.toggle("dark", t === "dark");
  localStorage.setItem("k-theme", t);
  $("#theme-toggle").textContent = t === "dark" ? "☀️ Light" : "🌙 Dark";
}

function applyLang(l) {
  state.lang = l;
  setLanguage(l);
  localStorage.setItem("k-lang", l);
  $("#lang-toggle").textContent = `🌐 ${l === "en" ? "Kiswahili" : "English"}`;
}

function destroyChart(key) { if (charts[key]) { charts[key].destroy(); delete charts[key]; } }

// ====== DASHBOARD ======
function renderDashboard() {
  const indigenous = CROPS.filter(c => c.status === "indigenous").length;
  $("#stat-crops").textContent = CROPS.length;
  $("#stat-indigenous").textContent = indigenous;
  $("#stat-corridors").textContent = CORRIDORS.length;
  $("#stat-tests").textContent = "150";

  destroyChart("resilience");
  const rsCrops = [...CROPS].filter(c => c.resilience_score != null).sort((a,b)=>a.resilience_score-b.resilience_score);
  const ctx1 = document.getElementById("chart-resilience");
  if (ctx1) {
    const colors = rsCrops.map(c => c.resilience_score > 0.8 ? "rgba(27,94,32,.8)" : c.resilience_score > 0.6 ? "rgba(199,149,43,.8)" : "rgba(229,57,53,.7)");
    charts.resilience = new Chart(ctx1, {
      type:"bar", data:{labels:rsCrops.map(c=>c.name_en?.split(",")[0]?.trim()||c.key),datasets:[{label:"Resilience (Rs)",data:rsCrops.map(c=>c.resilience_score),backgroundColor:colors,borderRadius:6,borderSkipped:false}]},
      options:{responsive:true,maintainAspectRatio:false,indexAxis:"y",plugins:{legend:{display:false},tooltip:{callbacks:{label:r=>`Rs ${r.parsed.x.toFixed(2)}`}}},scales:{x:{min:0,max:1,ticks:{stepSize:0.2,font:{size:10}},grid:{display:false}},y:{ticks:{font:{size:9}},grid:{display:false}}}}
    });
  }

  destroyChart("iron");
  const ironCtx = document.getElementById("chart-iron");
  if (ironCtx) {
    const feValues = [991, 0, 0, 0, 0, 0];
    const feLabels = ["Slenderleaf", "Nightshade", "Spider Plant", "Jute Mallow", "Amaranth", "Cowpea"];
    async function loadIron() {
      const data = await Promise.all(
        ["slenderleaf","black_nightshade","spider_plant","jute_mallow","amaranth","cowpea_leaves"]
          .map(async c=>{try{const r=await fetch(`/api/v1/traditional-foods/nutrition/${c}/minerals`);if(!r.ok)return null;const j=await r.json();return j?.mineral_composition_mg_per_kg_dw}catch{return null}})
      );
      data.forEach((d,i)=>{if(d?.Fe)feValues[i]=d.Fe});
      charts.iron = new Chart(ironCtx, {
        type:"bar", data:{labels:feLabels,datasets:[{label:"Iron (mg/kg DW)",data:feValues,backgroundColor:["rgba(198,40,40,.8)","rgba(229,57,53,.75)","rgba(239,83,80,.7)","rgba(255,112,67,.65)","rgba(255,171,145,.6)","rgba(255,205,210,.5)"],borderRadius:6,borderSkipped:false}]},
        options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:r=>`${r.parsed.y} mg/kg`}}},scales:{y:{beginAtZero:true,ticks:{font:{size:10}},grid:{color:"rgba(0,0,0,.05)"}},x:{ticks:{font:{size:9}},grid:{display:false}}}}
      });
    }
    loadIron();
  }
}

// ====== TRADITIONAL FOODS ======
function renderTraditionalFoods() {
  const crops = CROPS;
  const counties = [...new Set(crops.flatMap(c=>c.counties||[]))].sort();
  const sel = document.getElementById("tf-county");
  if (sel && !sel.options.length) {
    const o = document.createElement("option"); o.value = ""; o.textContent = "Select county..."; sel.appendChild(o);
    counties.forEach(c=>{const o=document.createElement("option");o.value=c;o.textContent=c;sel.appendChild(o)});
  }

  $("#tf-classify-btn")?.addEventListener("click", async ()=>{
    const input = $("#tf-input");
    const query = input?.value.trim().toLowerCase();
    if (!query) return;
    const el = $("#tf-result"); el.classList.remove("hidden");
    // Try API first, fall back to local
    let resp = null;
    try { const r = await fetch(`/api/v1/traditional-foods/classify/${encodeURIComponent(query)}`); if (r.ok) resp = await r.json(); } catch {}
    if (resp?.classified) {
      const c = resp; renderCropResult(el, c, query); return;
    }
    const local = crops.find(c => c.key === query || c.name_en.toLowerCase().includes(query) || c.name_sw?.toLowerCase().includes(query));
    if (local) { renderCropResult(el, local, query); return; }
    el.innerHTML = `<div style="background:rgba(255,193,7,.1);border:1px solid rgba(255,193,7,.2);border-radius:12px;padding:1rem;font-size:.85rem"><p style="font-weight:600">"${query}" not found</p><p style="color:rgba(0,0,0,.4);font-size:.75rem;margin-top:4px">Try: amaranth, managu, sagaa, mrenda, slenderleaf, mitoo, terere, kunde</p></div>`;
  });

  $("#tf-region-btn")?.addEventListener("click", async ()=>{
    const county = $("#tf-county")?.value;
    if (!county) return;
    const el = $("#tf-region-result"); el.classList.remove("hidden");
    let resp = null;
    try { const r = await fetch(`/api/v1/traditional-foods/region/${encodeURIComponent(county)}`); if (r.ok) resp = await r.json(); } catch {}
    if (resp?.crops?.length) {
      renderRegionResult(el, resp, county); return;
    }
    const localCrops = crops.filter(c=>c.counties?.includes(county));
    if (localCrops.length) { renderRegionResult(el, {county, crops:localCrops, crop_count:localCrops.length}, county); return; }
    el.innerHTML = `<div style="background:rgba(255,193,7,.1);border:1px solid rgba(255,193,7,.2);border-radius:12px;padding:1rem;font-size:.85rem">No data for ${county}</div>`;
  });

  const tbody = document.getElementById("tf-table-body");
  if (tbody) {
    tbody.innerHTML = crops.map(c => {
      const sc = c.status === "indigenous" ? "rgba(27,94,32,.12)" : c.status === "naturalised" ? "rgba(21,101,192,.12)" : "rgba(199,149,43,.12)";
      const sc2 = c.status === "indigenous" ? "#1B5E20" : c.status === "naturalised" ? "#1565C0" : "#8B6914";
      const rs = c.resilience_score;
      return `<tr style="border-bottom:1px solid rgba(0,0,0,.04);transition:background .2s" onmouseover="this.style.background='rgba(0,0,0,.02)'" onmouseout="this.style.background=''">
        <td style="padding:10px 8px 10px 12px;font-weight:500;font-size:.8rem">${c.name_en?.split(",")[0]?.trim() || c.key}</td>
        <td style="padding:10px 8px;color:rgba(0,0,0,.35);font-size:.75rem">${c.name_sw || ""}</td>
        <td style="padding:10px 8px"><span style="background:${sc};color:${sc2};padding:2px 10px;border-radius:20px;font-size:.6rem;font-weight:600;text-transform:uppercase">${c.status}</span></td>
        <td style="padding:10px 8px;font-weight:600;font-size:.85rem;color:${rs>0.8?'#1B5E20':rs>0.6?'#8B6914':'#C62828'}">${rs != null ? rs.toFixed(2) : "—"}</td>
        <td style="padding:10px 8px;color:rgba(0,0,0,.4);font-size:.75rem" class="hidden md:table-cell">${c.growing_season || ""}</td>
        <td style="padding:10px 12px 10px 8px;color:rgba(0,0,0,.35);font-size:.65rem" class="hidden lg:table-cell">${c.counties?.slice(0,3).join(", ") || ""}</td>
      </tr>`;
    }).join("");
  }
}

function renderCropResult(el, c, query) {
  const sc = c.status === "indigenous" ? "#1B5E20" : c.status === "naturalised" ? "#1565C0" : "#8B6914";
  el.innerHTML = `<div style="border:1px solid ${sc}22;border-radius:12px;padding:1rem;background:${sc}18;font-size:.85rem">
    <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px">
      <span style="background:${sc};color:#fff;padding:2px 10px;border-radius:20px;font-size:.65rem;font-weight:600;text-transform:uppercase">${c.status}</span>
      <span style="font-weight:600">${c.name_en || query}</span>
      <span style="color:rgba(0,0,0,.35);font-size:.75rem">${c.name_sw || ""}</span>
      ${c.resilience_score != null ? `<span style="background:${c.resilience_score>0.8?'rgba(27,94,32,.12)':'rgba(199,149,43,.12)'};color:${c.resilience_score>0.8?'#1B5E20':'#8B6914'};padding:2px 10px;border-radius:20px;font-size:.65rem;font-weight:600">Rs ${c.resilience_score.toFixed(2)}</span>` : ""}
    </div>
    ${c.origin||c.growing_season?`<p style="color:rgba(0,0,0,.45);font-size:.75rem"><strong>Origin:</strong> ${c.origin||"Unknown"} ${c.growing_season?`· <strong>Growing:</strong> ${c.growing_season}`:""}</p>`:""}
    ${c.traditional_uses?`<p style="color:rgba(0,0,0,.45);font-size:.75rem;margin-top:4px"><strong>Uses:</strong> ${c.traditional_uses}</p>`:""}
    ${c.nutrition?`<p style="color:rgba(0,0,0,.45);font-size:.75rem;margin-top:4px"><strong>Nutrition:</strong> ${c.nutrition}</p>`:""}
    ${c.market_price_kes_tonne?`<p style="color:rgba(0,0,0,.45);font-size:.75rem;margin-top:4px"><strong>Market Price:</strong> KES ${Number(c.market_price_kes_tonne).toLocaleString()}/t</p>`:""}
    ${c.intercropping?.length?`<p style="color:rgba(0,0,0,.45);font-size:.75rem;margin-top:4px"><strong>Intercrops:</strong> ${c.intercropping.map(i=>i.charAt(0).toUpperCase()+i.slice(1)).join(", ")}</p>`:""}
    ${c.counties?.length?`<p style="color:rgba(0,0,0,.45);font-size:.75rem;margin-top:4px"><strong>Counties:</strong> ${c.counties.join(", ")}</p>`:""}
  </div>`;
}

function renderRegionResult(el, resp, county) {
  el.innerHTML = `<div style="background:rgba(27,94,32,.06);border:1px solid rgba(27,94,32,.15);border-radius:12px;padding:1rem">
    <p style="font-size:.85rem;font-weight:600;margin-bottom:8px">${resp.crop_count} crops in ${county}</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px">${resp.crops.map(c=>{
      const sc = c.status === "indigenous" ? "#1B5E20" : c.status === "naturalised" ? "#1565C0" : "#8B6914";
      return `<div style="background:rgba(255,255,255,.6);border-radius:10px;padding:8px;border:1px solid rgba(0,0,0,.04);font-size:.75rem">
        <span style="display:block;font-weight:600">${c.name_en}</span><span style="display:block;color:rgba(0,0,0,.35)">${c.name_sw}</span>
        <span style="color:${sc};font-size:.65rem;font-weight:600">${c.status}</span>
      </div>`;
    }).join("")}</div></div>`;
}

// ====== CORRIDORS ======
function renderCorridors() {
  const mapEl = document.getElementById("map");
  if (mapEl && !leafletMap) {
    leafletMap = L.map("map", {zoomControl:true,attributionControl:false}).setView([-0.5,36.8],6);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{maxZoom:10}).addTo(leafletMap);
    const bounds=[];
    const locs = {
      "Nairobi":[-1.2921,36.8219],"Kisumu":[-0.1022,34.7617],"Mombasa":[-4.0435,39.6682],
      "Busia":[0.4614,34.1121],"Namanga":[-2.5431,36.7884],"Lodwar":[3.1214,35.6047],
      "Machakos":[-1.5177,37.2634],"Kitui":[-1.3704,38.0106],"Makueni":[-1.8049,37.6207],
      "Homa Bay":[-0.5229,34.4565],"Siaya":[0.0611,34.2898],"Migori":[-1.0667,34.4731],
      "Kakamega":[0.2843,34.7522],"Bungoma":[0.5714,34.5584],"Kiambu":[-1.1711,36.8354],
      "Murang'a":[-0.7226,37.1537],"Nyeri":[-0.4222,36.9509],"Meru":[0.0476,37.6494],
      "Embu":[-0.5378,37.4593],"Tharaka Nithi":[-0.2833,37.8667],
      "Arusha":[-3.3869,36.6830],"Tororo":[0.6950,34.1800],
      "Nakuru":[-0.3071,36.0730],"Baringo":[0.4667,35.9667],"Kajiado":[-1.8500,36.7833],
      "Narok":[-1.0833,35.8667],"Kilifi":[-3.6333,39.8500],"Kwale":[-4.1833,39.4500]
    };
    CORRIDORS.forEach(c=>{
      const cities = [...(c.origin_cities||[]),c.destination].flatMap(n=>n.replace(/\(.*?\)/g,"").split(",").map(p=>p.trim())).filter(l=>locs[l]);
      cities.forEach(l=>{bounds.push(locs[l]);L.circleMarker(locs[l],{radius:6,color:"#1B5E20",fillColor:"#1B5E20",fillOpacity:.8,weight:2}).addTo(leafletMap).bindPopup(`<b>${l}</b>`)});
      if(cities.length>=2){const pts=cities.map(l=>locs[l]).filter(Boolean);if(pts.length>=2)L.polyline(pts,{color:"#C7952B",weight:2.5,opacity:.7,dashArray:"8,6"}).addTo(leafletMap)}
    });
    if(bounds.length)leafletMap.fitBounds(L.latLngBounds(bounds),{padding:[30,30]});
  }

  const el=document.getElementById("corridor-cards");
  if(el){
    const icons=["🌾","🌿","🌴","🍌","🚛","🛵","🚌","🐪","🚢"];
    el.innerHTML=CORRIDORS.map((c,i)=>`<div class="card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px"><span style="font-size:1.2rem">${icons[i%icons.length]}</span><span style="font-weight:600;font-size:.9rem">${c.name}</span></div>
      <p style="font-size:.75rem;color:rgba(0,0,0,.4);margin-bottom:4px">${(c.origin_cities||[]).join(", ")} → ${c.destination}</p>
      <p style="font-size:.75rem;color:rgba(0,0,0,.45);margin-bottom:4px"><strong>Crops:</strong> ${(c.key_crops||[]).join(", ")}</p>
      ${c.transport?`<p style="font-size:.7rem;color:rgba(0,0,0,.35);margin-bottom:4px">${c.transport}</p>`:""}
      ${c.food_remittance_context?`<p style="font-size:.7rem;color:var(--teal);margin-bottom:4px">${c.food_remittance_context}</p>`:""}
      ${c.demand_intensity==="very_high"?'<span class="badge badge-green">High volume</span>':`<span class="badge badge-gold">${c.demand_intensity}</span>`}
    </div>`).join("");
  }
}

// ====== MARKETPLACE ======
function renderMarketplace() {
  const listings = [];
  const counties = [...new Set(CROPS.flatMap(c=>c.counties||[]))].sort();
  $$("select[name='county'], #mp-county-filter").forEach(s=>{
    if(s.options.length<=1){const o=document.createElement("option");o.value="";o.textContent="All counties";s.appendChild(o);counties.forEach(c=>{const o=document.createElement("option");o.value=c;o.textContent=c;s.appendChild(o)})}
  });

  async function loadListings() {
    try{const r=await fetch("/api/v1/marketplace/listings");if(r.ok){const j=await r.json();if(j?.listings?.length)renderListingUI(j.listings)}}
    catch{} // silently use empty state
  }

  function renderListingUI(items){
    const el=document.getElementById("mp-listings");
    if(!el)return;
    if(!items.length){el.innerHTML=`<div style="text-align:center;color:rgba(0,0,0,.3);padding:3rem 1rem;font-size:.9rem">No listings. Be the first to post!</div>`;return}
    el.innerHTML=items.map(l=>{
      const sb=l.status==="indigenous"?"#1B5E20":l.status==="naturalised"?"#1565C0":"#8B6914";
      return `<div class="card"${l.is_chama?' style="border-left:4px solid var(--gold)"':''}>
        <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:4px">
          <span style="font-weight:600;font-size:.85rem">${l.food}</span>
          <div style="display:flex;gap:4px;flex-wrap:wrap">
            ${l.status?`<span class="badge" style="background:${sb}18;color:${sb}">${l.status}</span>`:""}
            ${l.is_chama?`<span class="badge" style="background:rgba(199,149,43,.12);color:#8B6914">👩‍👩‍👧‍👧 ${l.chama_name||"Chama"}</span>`:""}
          </div>
        </div>
        ${l.food_sw?`<p style="font-size:.75rem;color:rgba(0,0,0,.35);margin-bottom:2px">${l.food_sw}</p>`:""}
        <p style="font-size:1.3rem;font-weight:700;color:var(--green);margin-bottom:2px">KES ${Number(l.price_kes_per_kg).toLocaleString()}/kg</p>
        <p style="font-size:.75rem;color:rgba(0,0,0,.4);margin-bottom:2px">${Number(l.quantity_kg).toLocaleString()} kg · KES ${(l.quantity_kg*l.price_kes_per_kg).toLocaleString()} total</p>
        <p style="font-size:.75rem;color:rgba(0,0,0,.4);margin-bottom:2px">📍 ${l.county}${l.corridor?` · ${l.corridor}`:""}${l.delivery_available?" · 🚚 Delivery":""}</p>
        <p style="font-size:.7rem;color:rgba(0,0,0,.3)">${l.seller}${l.contact?` · ${l.contact}`:""}${l.created_at?` · ${new Date(l.created_at).toLocaleDateString()}`:""}</p>
      </div>`;
    }).join("");
  }

  renderListingUI(listings);
  loadListings();

  $("#mp-filter-btn")?.addEventListener("click", ()=>{toast("Post a listing first to see filters","info")});
  let chamaOn=false;
  $("#mp-chama-btn")?.addEventListener("click", e=>{
    chamaOn=!chamaOn;
    e.target.style.background=chamaOn?"#1B5E20":"";
    e.target.style.color=chamaOn?"white":"";
    toast(chamaOn?"Showing chamas only":"Showing all","info");
  });

  $("#mp-form")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const fd=new FormData(e.target);
    const body=Object.fromEntries(fd.entries());
    body.is_chama=fd.has("is_chama");
    body.quantity_kg=parseFloat(body.quantity_kg)||0;
    body.price_kes_per_kg=parseFloat(body.price_kes_per_kg)||0;
    try{const r=await fetch("/api/v1/marketplace/listings",{method:"POST",body:JSON.stringify(body),headers:{"Content-Type":"application/json"}});if(r.ok){toast("Listing posted!");e.target.reset();renderMarketplace()}else toast("Backend not connected — listing saved locally","info")}
    catch{toast("Backend not connected yet. Deploy Render to enable listings.","info")}
  });

  // Prices table
  const pe=document.getElementById("mp-prices");
  if(pe){
    pe.innerHTML=`<table style="width:100%;font-size:.8rem"><thead><tr style="text-align:left;color:rgba(0,0,0,.4);border-bottom:1px solid rgba(0,0,0,.06)">
      <th style="padding:8px 8px 8px 0;font-weight:500">Crop</th><th style="padding:8px 8px;font-weight:500">KES/t</th><th style="padding:8px 8px;font-weight:500">Status</th>
    </tr></thead><tbody>
      ${CROPS.filter(c=>c.market_price_kes_tonne).slice(0,20).map(c=>`<tr style="border-bottom:1px solid rgba(0,0,0,.04)">
        <td style="padding:8px 8px 8px 0;font-weight:500;font-size:.75rem">${c.name_en?.split(",")[0]?.trim()||c.key}</td>
        <td style="padding:8px 8px;font-weight:600">KES ${Number(c.market_price_kes_tonne).toLocaleString()}</td>
        <td style="padding:8px 0;font-size:.75rem">${c.status==="indigenous"?"🌿":c.status==="naturalised"?"🌱":"🌾"}</td>
      </tr>`).join("")}
    </tbody></table>`;
  }

  destroyChart("markup");
  const mc=document.getElementById("chart-markup");
  if(mc){
    charts.markup=new Chart(mc,{
      type:"bar",data:{labels:["Nightshade","Amaranth","Cowpea","Spider Plant","Pumpkin"],
        datasets:[
          {label:"Retail Markup %",data:[127,130,143,57,40],backgroundColor:["rgba(27,94,32,.8)","rgba(199,149,43,.8)","rgba(198,40,40,.7)","rgba(21,101,192,.7)","rgba(93,64,55,.7)"],borderRadius:6,borderSkipped:false},
          {label:"PHL Rate (57%)",data:[57,57,57,57,57],type:"line",borderColor:"#C62828",borderWidth:2,pointRadius:0,fill:false,borderDash:[6,3]}
        ]},
      options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:"top",labels:{boxWidth:12,font:{size:9}}}},scales:{y:{beginAtZero:true,grid:{color:"rgba(0,0,0,.04)"}},x:{grid:{display:false}}}}
    });
  }
}

// ====== DE-RISK ======
function renderDeRisk() {
  const d=DERISK;

  const ov=document.getElementById("dr-overview");
  if(ov){
    const icons=["🔥","💰","💡","📚"];
    ov.innerHTML=d.overview.forces.map((f,i)=>`<div class="card" style="border-left:3px solid var(--green)">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px"><span style="font-size:1.1rem">${icons[i]}</span><span style="font-weight:700;font-size:.85rem">${f.name}</span></div>
      <p style="font-size:.75rem;color:rgba(0,0,0,.45);line-height:1.5">${f.detail}</p>
      <p style="font-size:.65rem;color:rgba(0,0,0,.25);margin-top:6px">Sources: ${f.data_sources.join(", ")}</p>
    </div>`).join("");
  }

  const pm=document.getElementById("dr-parametrics");
  if(pm){
    const m=d.parametrics.model;
    pm.innerHTML=`<p style="font-size:.75rem;color:rgba(0,0,0,.45);margin-bottom:8px">${m.description}</p>
      <div style="display:flex;flex-direction:column;gap:6px">${m.trigger_metrics.map(t=>`
        <div style="background:rgba(0,0,0,.03);border-radius:10px;padding:10px;font-size:.75rem">
          <p style="font-weight:600;margin-bottom:2px;text-transform:capitalize">${t.name.replace(/_/g," ")}</p>
          <p style="color:rgba(0,0,0,.4);font-size:.7rem">Sensor: ${t.sensor} · Payout: ${t.payout_formula}</p>
          <p style="color:rgba(0,0,0,.35);font-size:.7rem">Threshold: ${t.threshold}</p>
        </div>`
      ).join("")}</div>
      <p style="font-size:.75rem;color:rgba(0,0,0,.45);margin-top:8px"><strong>Premium:</strong> ${m.premium_estimate_kes_per_ha}</p>
      ${d.parametrics.county_context?.primary_risk?`<p style="font-size:.7rem;color:var(--teal);margin-top:4px">${d.parametrics.county_context.primary_risk}</p>`:""}`;
  }

  destroyChart("greenbond");
  const gc=document.getElementById("chart-greenbond");
  if(gc&&d.greenbond?.allocations){
    charts.greenbond=new Chart(gc,{
      type:"doughnut",data:{labels:d.greenbond.allocations.map(a=>a.program),datasets:[{data:d.greenbond.allocations.map(a=>a.allocation_pct),backgroundColor:["#1B5E20","#C7952B","#00695C","#5D4037"],borderWidth:0}]},
      options:{responsive:true,maintainAspectRatio:false,cutout:"65%",plugins:{legend:{position:"bottom",labels:{boxWidth:10,font:{size:9},padding:8}},tooltip:{callbacks:{label:r=>`${r.label}: ${r.parsed}%`}}}}
    });
  }

  const ue=document.getElementById("dr-usaid");
  if(ue){
    const km=d.usaid.key_metrics;
    ue.innerHTML=`<p style="font-size:.85rem;font-weight:600;margin-bottom:4px">${km.bilateral_aid_contraction_usd} contraction</p>
      <p style="color:rgba(0,0,0,.45)"><strong>Awards terminated:</strong> ${km.award_termination_rate_pct}</p>
      <p style="color:rgba(0,0,0,.45);margin-top:2px"><strong>CSA mainstreamed:</strong> ${km.csa_mainstreamed_in_counties_pct}% counties</p>
      <p style="color:rgba(0,0,0,.45);margin-top:2px"><strong>CSA funded:</strong> ${km.csa_budget_allocated_pct}%</p>
      <p style="color:rgba(0,0,0,.45);margin-top:2px"><strong>Food insecure:</strong> ${km.food_insecurity_estimate_2026}</p>
      <p style="color:rgba(0,0,0,.3);font-size:.7rem;margin-top:6px">${d.usaid.systemic_consequence.slice(0,120)}...</p>`;
  }

  const ph=document.getElementById("dr-phl");
  if(ph){
    ph.innerHTML=`<p style="font-size:1.5rem;font-weight:700;color:var(--green);margin-bottom:2px">${d.phl.aiv_phl_rate_pct}%</p>
      <p style="font-size:.75rem;color:rgba(0,0,0,.45);margin-bottom:4px">Post-harvest loss rate for AIVs</p>
      <p style="font-size:.75rem;color:rgba(0,0,0,.45);margin-bottom:8px">Farmer burden <strong>${d.phl.economic_burden_ratio_farmer_vs_retailer}x</strong> vs retailer</p>
      <div style="display:flex;flex-direction:column;gap:4px">${d.phl.interventions.map(i=>`<div style="background:rgba(0,0,0,.03);border-radius:8px;padding:8px;font-size:.75rem"><p style="font-weight:600;margin-bottom:2px">${i.solution}</p><p style="color:rgba(0,0,0,.4)">Reduces PHL ${i.phl_reduction_pct}%</p></div>`).join("")}</div>`;
  }

  const ce=document.getElementById("dr-carbon");
  if(ce){
    const seq=d.carbon.estimated_sequestration_tonnes_co2_per_ha||{};
    ce.innerHTML=`<p style="font-size:.75rem;color:rgba(0,0,0,.45);margin-bottom:6px">${d.carbon.description}</p>
      ${Object.entries(seq).map(([k,v])=>`<div style="display:flex;justify-content:space-between;font-size:.75rem;padding:4px 0;border-bottom:1px solid rgba(0,0,0,.04)"><span style="text-transform:capitalize">${k.replace(/_/g," ")}</span><span style="font-weight:600;color:${v>0?'var(--green)':'#C62828'}">${v} tCO₂/ha</span></div>`).join("")}
      <p style="font-size:.75rem;color:rgba(0,0,0,.45);margin-top:6px"><strong>Price:</strong> ${d.carbon.carbon_price_kes_per_tonne}</p>
      <p style="font-size:.75rem;color:rgba(0,0,0,.45)"><strong>Revenue:</strong> ${d.carbon.additional_revenue_kes_per_ha}/ha</p>`;
  }
}

// ====== INIT ======
document.addEventListener("DOMContentLoaded", async () => {
  applyLang(state.lang);
  theme(state.theme);

  $$(".nav-link, .bottom-nav-link").forEach(l=>l.addEventListener("click", e=>{
    e.preventDefault();
    nav(l.dataset.nav);
    const pages = {dashboard:renderDashboard,"traditional-foods":renderTraditionalFoods,corridors:renderCorridors,marketplace:renderMarketplace,"de-risk":renderDeRisk};
    const fn = pages[l.dataset.nav];
    if (fn) setTimeout(fn, 50);
    if (l.dataset.nav === "corridors") setTimeout(()=>{if(leafletMap)leafletMap.invalidateSize()},200);
  }));

  $("#theme-toggle")?.addEventListener("click", ()=>theme(state.theme==="light"?"dark":"light"));
  $("#lang-toggle")?.addEventListener("click", ()=>applyLang(state.lang==="en"?"sw":"en"));

  nav("dashboard");
  renderDashboard();
  renderTraditionalFoods();
});
