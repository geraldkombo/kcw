from __future__ import annotations

import pytest
from knowledge.traditional_foods import TraditionalFoodsIndex
from agriculture_intelligence.precision_farming import CROP_BASE_TEMPS, HARVEST_GDD_THRESHOLDS
from agriculture_intelligence.land_intelligence import LandIntelligence
from agriculture_intelligence.market_intelligence import MarketIntelligence


class TestTraditionalFoodsIndex:
    def setup_method(self):
        self.tfi = TraditionalFoodsIndex()

    def test_classify_indigenous_crop(self):
        result = self.tfi.classify_crop("managu")
        assert result is not None
        assert result["status"] == "indigenous"
        assert "Solanum" in result["origin"]

    def test_classify_by_swahili_name(self):
        result = self.tfi.classify_crop("terere")
        assert result is not None
        assert result["name_en"].startswith("Amaranth")

    def test_classify_by_english_name(self):
        result = self.tfi.classify_crop("spider plant")
        assert result is not None
        assert result["status"] == "indigenous"

    def test_classify_exotic_crop(self):
        result = self.tfi.classify_crop("kale")
        assert result is not None
        assert result["status"] == "exotic"

    def test_classify_unknown_returns_none(self):
        assert self.tfi.classify_crop("nonexistent_crop_xyz") is None

    def test_list_indigenous(self):
        crops = self.tfi.list_indigenous()
        assert len(crops) >= 8
        names = [c["name_en"] for c in crops]
        assert any("Amaranth" in n for n in names)
        assert any("nightshade" in n.lower() for n in names)

    def test_list_naturalised(self):
        crops = self.tfi.list_naturalised()
        assert len(crops) >= 3
        names = [c["name_en"] for c in crops]
        assert any("Cassava" in n for n in names)

    def test_list_exotic(self):
        crops = self.tfi.list_exotic()
        assert len(crops) >= 2
        names = [c["name_en"] for c in crops]
        assert any("Kale" in n for n in names)

    def test_list_all(self):
        crops = self.tfi.list_all()
        assert len(crops) >= 30

    def test_get_crops_for_region(self):
        crops = self.tfi.get_crops_for_region("kisumu")
        assert len(crops) >= 3
        names = [c["name_en"] for c in crops]
        assert any("nightshade" in n.lower() for n in names)

    def test_get_crops_for_ukambani(self):
        crops = self.tfi.get_crops_for_region("machakos")
        assert len(crops) >= 3
        names = [c["name_en"] for c in crops]
        assert any("Cowpea" in n for n in names)

    def test_intercropping_patterns(self):
        patterns = self.tfi.get_intercropping_patterns()
        assert len(patterns) >= 10
        names = [p["name"] for p in patterns]
        assert any("Lake Region" in n for n in names)
        assert any("Ukambani" in n for n in names)

    def test_intercropping_by_county(self):
        patterns = self.tfi.get_intercropping_patterns("kisumu")
        assert len(patterns) >= 1
        assert "Lake Region" in patterns[0]["name"]

    def test_food_corridors(self):
        corridors = self.tfi.get_food_corridors()
        assert len(corridors) >= 8

    def test_food_corridor_by_county(self):
        corridors = self.tfi.get_food_corridors("kisumu")
        assert len(corridors) >= 1
        assert "Luo" in corridors[0]["name"]

    def test_nutritional_context_indigenous(self):
        ctx = self.tfi.get_nutritional_context("managu")
        assert ctx["status"] == "indigenous"
        assert "naturally adapted" in ctx["value_proposition"]

    def test_nutritional_context_exotic(self):
        ctx = self.tfi.get_nutritional_context("kale")
        assert ctx["status"] == "exotic"
        assert "higher inputs" in ctx["value_proposition"]

    def test_resilience_rating_high(self):
        rating = self.tfi.get_resilience_rating(["managu", "terere", "kunde"])
        assert rating["indigenous_crop_ratio"] > 0.5
        assert rating["resilience_score"] > 0.6

    def test_resilience_rating_low(self):
        rating = self.tfi.get_resilience_rating(["maize", "kale", "cabbage"])
        assert rating["indigenous_crop_ratio"] == 0.0
        assert "higher input" in rating["note"]

    def test_resilience_score_in_all_crops(self):
        for key, info in self.tfi.CROP_INDEX.items():
            assert "resilience_score" in info, f"{key} missing resilience_score"
            assert 0.0 <= info["resilience_score"] <= 1.0

    def test_nutrition_minerals_indigenous(self):
        ctx = self.tfi.get_nutrition_minerals("managu")
        assert ctx["status"] == "indigenous"
        assert "mineral_composition_mg_per_kg_dw" in ctx
        assert ctx["iron_rich"] is True

    def test_nutrition_minerals_unknown(self):
        ctx = self.tfi.get_nutrition_minerals("wheat")
        assert ctx == {}

    def test_new_ojwang_crops_classifiable(self):
        for crop in ["slenderleaf", "mitoo", "desert_date", "mchunju", "bird_plum", "ekalale", "vitex_black_plum", "jwelu"]:
            result = self.tfi.classify_crop(crop)
            assert result is not None, f"{crop} not found"
            assert result["status"] == "indigenous"

    def test_new_cross_border_corridors(self):
        corridors = self.tfi.get_food_corridors()
        names = [c["name"] for c in corridors]
        assert any("Uganda" in n for n in names), "Busia corridor missing"
        assert any("Tanzania" in n for n in names), "Namanga corridor missing"
        assert any("Turkana" in n for n in names), "Turkana corridor missing"


class TestIndigenousCropsInPrecisionFarming:
    def test_amaranth_in_crop_base_temps(self):
        assert "amaranth" in CROP_BASE_TEMPS
        assert CROP_BASE_TEMPS["amaranth"] == 15

    def test_black_nightshade_in_crop_base_temps(self):
        assert "black_nightshade" in CROP_BASE_TEMPS
        assert CROP_BASE_TEMPS["black_nightshade"] == 14

    def test_indigenous_crops_in_harvest_gdd(self):
        assert "amaranth" in HARVEST_GDD_THRESHOLDS
        assert "black_nightshade" in HARVEST_GDD_THRESHOLDS
        assert "spider_plant" in HARVEST_GDD_THRESHOLDS
        assert "cowpea_leaves" in HARVEST_GDD_THRESHOLDS

    def test_indigenous_gdd_values_reasonable(self):
        assert HARVEST_GDD_THRESHOLDS["amaranth"] < 1000
        assert HARVEST_GDD_THRESHOLDS["pigeon_pea"] > 1000
        assert HARVEST_GDD_THRESHOLDS["baobab"] == 3650


class TestIndigenousCropsInLandIntelligence:
    def setup_method(self):
        self.li = LandIntelligence(power=None)

    def test_amaranth_in_crop_requirements(self):
        assert "amaranth" in self.li.CROP_REQUIREMENTS

    def test_indigenous_vegetables_in_requirements(self):
        for crop in ["amaranth", "black_nightshade", "spider_plant", "cowpea_leaves"]:
            assert crop in self.li.CROP_REQUIREMENTS, f"{crop} missing from CROP_REQUIREMENTS"

    def test_indigenous_grains_in_requirements(self):
        for crop in ["finger_millet", "sorghum", "pigeon_pea", "amaranth"]:
            assert crop in self.li.CROP_REQUIREMENTS, f"{crop} missing from CROP_REQUIREMENTS"

    def test_dryland_crops_in_requirements(self):
        for crop in ["cowpea_leaves", "pigeon_pea", "bambara_nut"]:
            assert crop in self.li.CROP_REQUIREMENTS, f"{crop} missing from CROP_REQUIREMENTS"
            req = self.li.CROP_REQUIREMENTS[crop]
            assert req["temp_max"] >= 35, f"{crop} should tolerate high temps"
            assert req["precip_min"] <= 2.0, f"{crop} should be drought-tolerant"

    def test_fruit_trees_in_requirements(self):
        for crop in ["baobab", "tamarind"]:
            assert crop in self.li.CROP_REQUIREMENTS, f"{crop} missing"
            req = self.li.CROP_REQUIREMENTS[crop]
            assert req["soil_moisture_min"] <= 0.1, f"{crop} should tolerate low moisture"
            assert req["growing_days"] == 365, f"{crop} should have full-year growing cycle"


class TestIndigenousCropsInMarketIntelligence:
    def setup_method(self):
        self.mi = MarketIntelligence(power=None)

    def test_indigenous_veg_market_prices(self):
        for crop in ["amaranth", "black_nightshade", "spider_plant"]:
            assert crop in self.mi.MARKET_PRICES, f"{crop} missing from MARKET_PRICES"
            assert self.mi.MARKET_PRICES[crop]["current"] > 0

    def test_baobab_has_premium_price(self):
        assert "baobab" in self.mi.MARKET_PRICES
        assert self.mi.MARKET_PRICES["baobab"]["current"] > 100000

    def test_indigenous_grain_prices(self):
        assert "finger_millet" in self.mi.MARKET_PRICES
        assert self.mi.MARKET_PRICES["finger_millet"]["current"] > 50000

    def test_indigenous_trends(self):
        for crop in ["amaranth", "black_nightshade", "finger_millet"]:
            assert self.mi.MARKET_PRICES[crop]["trend"] in ("up", "stable", "down")
