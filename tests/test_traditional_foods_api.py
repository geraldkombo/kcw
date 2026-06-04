from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_classify_indigenous_crop(client):
    resp = client.get("/api/v1/traditional-foods/classify/amaranth")
    assert resp.status_code == 200
    data = resp.json()
    assert data["classified"] is True
    assert data["status"] == "indigenous"


def test_classify_exotic_crop(client):
    resp = client.get("/api/v1/traditional-foods/classify/kale")
    assert resp.status_code == 200
    data = resp.json()
    assert data["classified"] is True
    assert data["status"] == "exotic"


def test_classify_unknown_crop(client):
    resp = client.get("/api/v1/traditional-foods/classify/wheat")
    assert resp.status_code == 200
    data = resp.json()
    assert data["classified"] is False


def test_list_all_crops(client):
    resp = client.get("/api/v1/traditional-foods/list")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] >= 30
    assert data["status_filter"] == "all"


def test_list_indigenous_crops(client):
    resp = client.get("/api/v1/traditional-foods/list?status=indigenous")
    assert resp.status_code == 200
    data = resp.json()
    for c in data["crops"]:
        assert c["status"] == "indigenous"


def test_crops_by_region(client):
    resp = client.get("/api/v1/traditional-foods/region/Kisumu")
    assert resp.status_code == 200
    data = resp.json()
    assert data["county"] == "Kisumu"
    assert data["crop_count"] > 0
    for c in data["crops"]:
        assert "name_sw" in c
        assert "name_en" in c


def test_crops_by_unknown_region(client):
    resp = client.get("/api/v1/traditional-foods/region/Atlantis")
    assert resp.status_code == 200
    data = resp.json()
    assert data["crop_count"] == 0


def test_intercropping_patterns(client):
    resp = client.get("/api/v1/traditional-foods/intercropping")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] >= 1
    assert len(data["patterns"]) >= 1


def test_food_corridors(client):
    resp = client.get("/api/v1/traditional-foods/corridors")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] >= 1


def test_resilience_rating(client):
    resp = client.get("/api/v1/traditional-foods/resilience?crops=amaranth,black%20nightshade")
    assert resp.status_code == 200
    data = resp.json()
    assert "resilience_score" in data
    assert "indigenous_crop_ratio" in data


def test_nutritional_context(client):
    resp = client.get("/api/v1/traditional-foods/nutrition/amaranth")
    assert resp.status_code == 200
    data = resp.json()
    if "note" not in data:
        assert "crop" in data


def test_graphrag_known_crops_include_traditional():
    from graphrag.service import KNOWN_CROPS

    assert "amaranth" in KNOWN_CROPS
    assert "black nightshade" in KNOWN_CROPS
    assert "spider plant" in KNOWN_CROPS
    assert "finger millet" in KNOWN_CROPS
    assert "baobab" in KNOWN_CROPS
    assert "tamarind" in KNOWN_CROPS
    assert "bambara nut" in KNOWN_CROPS


def test_nutrition_minerals_endpoint(client):
    resp = client.get("/api/v1/traditional-foods/nutrition/slenderleaf/minerals")
    assert resp.status_code == 200
    data = resp.json()
    assert "iron_rich" in data
    assert data["iron_rich"] is True


def test_new_ojwang_crops_classify(client):
    for crop in ["slenderleaf", "desert_date", "bird_plum", "mitoo"]:
        resp = client.get(f"/api/v1/traditional-foods/classify/{crop}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["classified"] is True
        assert data["status"] == "indigenous"


def test_all_corridors_in_api(client):
    resp = client.get("/api/v1/traditional-foods/corridors")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] >= 8
    names = [c["name"] for c in data["corridors"]]
    assert any("Uganda" in n for n in names)
    assert any("Tanzania" in n for n in names)
    assert any("Turkana" in n for n in names)
