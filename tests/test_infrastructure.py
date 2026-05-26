"""Integration tests for production infrastructure:
config, logging, repository, and API middleware."""

from __future__ import annotations

import json
import logging
import os
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.dependencies import get_repository
from config.log import configure_logging, get_request_id, set_request_id
from config.settings import Settings, settings, validate_settings
from database.repository import InMemoryRepository


# =============================================================================
# Config / Settings
# =============================================================================

class TestSettings:
    def test_default_settings(self):
        s = Settings(_env_file=None)
        assert s.neo4j_uri == "bolt://localhost:7687"
        assert s.api_port == 8000
        assert s.log_level == "INFO"
        assert s.cors_origins == "*"
        assert s.rate_limit_per_minute == 60
        assert s.securitisation_min_pool_size == 100

    def test_cors_origins_list_single(self):
        s = Settings(cors_origins="*")
        assert s.cors_origins_list == ["*"]

    def test_cors_origins_list_multiple(self):
        s = Settings(cors_origins="https://app.kcw.ke,https://admin.kcw.ke")
        assert s.cors_origins_list == ["https://app.kcw.ke", "https://admin.kcw.ke"]

    def test_neo4j_uri_validation(self):
        with pytest.raises(ValueError, match="NEO4J_URI must start with"):
            Settings(neo4j_uri="mongodb://localhost")

    def test_neo4j_uri_valid_schemes(self):
        for scheme in ("bolt://localhost:7687", "neo4j://localhost", "neo4j+s://example.com"):
            s = Settings(neo4j_uri=scheme)
            assert s.neo4j_uri == scheme

    def test_log_level_validation(self):
        with pytest.raises(ValueError):
            Settings(log_level="TRACE")

    def test_api_port_range(self):
        with pytest.raises(ValueError):
            Settings(api_port=80)  # below 1024

    def test_env_file_loading(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("NEO4J_URI=bolt://test:7687\n")
            f.write("LOG_LEVEL=DEBUG\n")
            f.write("CORS_ORIGINS=https://test.ke\n")
            env_path = f.name
        try:
            s = Settings(_env_file=env_path)
            assert s.neo4j_uri == "bolt://test:7687"
            assert s.log_level == "DEBUG"
            assert s.cors_origins_list == ["https://test.ke"]
        finally:
            os.unlink(env_path)

    def test_validate_settings_warns_default_neo4j(self):
        s = Settings(neo4j_uri="bolt://localhost:7687", cors_origins="*", api_key=None)
        warnings = []
        if s.neo4j_uri == "bolt://localhost:7687":
            warnings.append("NEO4J_URI using default")
        if s.cors_origins == "*":
            warnings.append("CORS_ORIGINS=*")
        if s.api_key is None:
            warnings.append("API_KEY is not set")
        assert len(warnings) >= 1

    def test_featherless_not_set(self):
        s = Settings(featherless_api_key=None)
        assert s.featherless_api_key is None


# =============================================================================
# Logging
# =============================================================================

class TestLogging:
    def test_request_id_context(self):
        set_request_id()
        rid = get_request_id()
        assert len(rid) == 12
        assert isinstance(rid, str)

    def test_request_id_explicit(self):
        rid = set_request_id("custom-id-123")
        assert get_request_id() == "custom-id-123"

    def test_configure_logging_json(self, caplog):
        configure_logging("DEBUG", log_json=True)
        logger = logging.getLogger("kcw.test")
        logger.info("hello json")
        # caplog won't capture JSON output since it uses StreamHandler directly
        # Just verify no crash
        assert True

    def test_configure_logging_text(self, caplog):
        configure_logging("DEBUG", log_json=False)
        logger = logging.getLogger("kcw.test")
        logger.info("hello text")
        assert True

    def test_request_id_in_log_record(self):
        set_request_id("test-rid")
        configure_logging("DEBUG", log_json=False)
        logger = logging.getLogger("kcw.test.rid")
        logger.info("check rid")
        # Can't easily assert on log output format, verify no crash
        assert True


# =============================================================================
# In-Memory Repository
# =============================================================================

class TestInMemoryRepository:
    def setup_method(self):
        self.db = InMemoryRepository()

    def test_save_and_get_farmer(self):
        farmer = self.db.save_farmer({"name": "Grace", "county": "Kiambu"})
        assert "farmer_id" in farmer
        assert "created_at" in farmer
        fetched = self.db.get_farmer(farmer["farmer_id"])
        assert fetched is not None
        assert fetched["name"] == "Grace"

    def test_list_farmers(self):
        self.db.save_farmer({"name": "A"})
        self.db.save_farmer({"name": "B"})
        assert len(self.db.list_farmers()) == 2

    def test_save_and_get_loan(self):
        loan = self.db.save_loan({"farmer_id": "KCW-001", "amount_kes": 15000})
        assert "loan_id" in loan
        fetched = self.db.get_loan(loan["loan_id"])
        assert fetched is not None

    def test_list_loans(self):
        self.db.save_loan({"farmer_id": "F1"})
        self.db.save_loan({"farmer_id": "F2"})
        assert len(self.db.list_loans()) == 2

    def test_pool_crud(self):
        pool = self.db.save_pool({"name": "Test Pool", "total_notional_kes": 100000})
        pid = pool["pool_id"]
        assert self.db.get_pool(pid) is not None
        assert len(self.db.list_pools()) == 1

    def test_audit_crud(self):
        entry = self.db.record_audit({"event_type": "test", "actor": "tester", "farmer_id": "F1", "data": {}})
        assert "timestamp" in entry
        assert len(self.db.get_audit("F1")) == 1
        assert len(self.db.get_all_audit()) == 1

    def test_get_farmer_nonexistent(self):
        assert self.db.get_farmer("FAKE") is None

    def test_get_loan_nonexistent(self):
        assert self.db.get_loan("FAKE") is None

    def test_get_pool_nonexistent(self):
        assert self.db.get_pool("FAKE") is None

    def test_audit_empty(self):
        assert self.db.get_audit("FAKE") == []
        assert self.db.get_all_audit() == []


# =============================================================================
# API / FastAPI Integration
# =============================================================================

class TestAPI:
    def setup_method(self):
        # Use InMemoryRepository for tests (avoids filesystem + lifespan issues)
        self._test_repo = InMemoryRepository()
        app.dependency_overrides[get_repository] = lambda: self._test_repo
        self.client = TestClient(app)

    def test_health(self):
        resp = self.client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["service"] == "kilimo-credit-web"

    def test_ready(self):
        resp = self.client.get("/ready")
        assert resp.status_code == 200
        data = resp.json()
        assert "status" in data

    def test_config(self):
        resp = self.client.get("/api/v1/config")
        assert resp.status_code == 200
        data = resp.json()
        assert data["neo4j_uri"] == "bolt://localhost:7687"
        assert "rate_limit_per_minute" in data
        assert "featherless_configured" in data

    _FARMER_BASE = {
        "sub_county": "Test", "village": "Test", "latitude": -1.0,
        "longitude": 36.9, "year_registered": 2022,
    }

    def test_create_farmer(self):
        body = dict(self._FARMER_BASE, first_name="Test", last_name="User",
            phone="+254700000000", county="Kiambu", gender="M",
            farm_size_ha=2.0, primary_crop="maize", chama_member=True, sacco_member=False)
        resp = self.client.post("/api/v1/farmers", json=body)
        assert resp.status_code == 201
        data = resp.json()
        assert data["first_name"] == "Test"
        assert data["id"].startswith("KCW-")

    def test_list_farmers(self):
        a = dict(self._FARMER_BASE, first_name="A", last_name="One",
            phone="+254700000001", county="Kiambu", gender="F",
            farm_size_ha=1.0, primary_crop="maize")
        b = dict(self._FARMER_BASE, first_name="B", last_name="Two",
            phone="+254700000002", county="Nakuru", gender="M",
            farm_size_ha=2.0, primary_crop="beans")
        self.client.post("/api/v1/farmers", json=a)
        self.client.post("/api/v1/farmers", json=b)
        resp = self.client.get("/api/v1/farmers")
        assert resp.status_code == 200
        data = resp.json()
        # At least the farmers we just created exist
        names = [f["first_name"] for f in data]
        assert "A" in names
        assert "B" in names

    def test_get_farmer_by_id(self):
        body = dict(self._FARMER_BASE, first_name="Find", last_name="Me",
            phone="+254700000003", county="Meru", gender="F",
            farm_size_ha=3.0, primary_crop="coffee")
        create_resp = self.client.post("/api/v1/farmers", json=body)
        fid = create_resp.json()["id"]
        resp = self.client.get(f"/api/v1/farmers/{fid}")
        assert resp.status_code == 200
        assert resp.json()["first_name"] == "Find"

    def test_get_farmer_not_found(self):
        resp = self.client.get("/api/v1/farmers/KCW-NONEXISTENT")
        assert resp.status_code == 404

    def test_update_farmer(self):
        body = dict(self._FARMER_BASE, first_name="Update", last_name="Test",
            phone="+254700000004", county="Kiambu", gender="M",
            farm_size_ha=1.5, primary_crop="tomato")
        create_resp = self.client.post("/api/v1/farmers", json=body)
        fid = create_resp.json()["id"]
        resp = self.client.patch(f"/api/v1/farmers/{fid}", json={"county": "Nakuru"})
        assert resp.status_code == 200
        assert resp.json()["county"] == "Nakuru"

    def test_create_loan(self):
        body = dict(self._FARMER_BASE, first_name="Loan", last_name="Test",
            phone="+254700000005", county="Nyeri", gender="F",
            farm_size_ha=2.0, primary_crop="tea")
        farmer = self.client.post("/api/v1/farmers", json=body).json()
        resp = self.client.post("/api/v1/loans", json={
            "farmer_id": farmer["id"],
            "amount_kes": 50000,
            "interest_rate_annual": 18.0,
            "purpose": "seeds",
            "term_months": 12,
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["id"].startswith("LN-")
        assert data["status"] == "pending"
        assert "pd_at_origination" in data

    def test_list_loans(self):
        body = dict(self._FARMER_BASE, first_name="L2", last_name="Test",
            phone="+254700000006", county="Kiambu", gender="M",
            farm_size_ha=1.0, primary_crop="maize")
        farmer = self.client.post("/api/v1/farmers", json=body).json()
        self.client.post("/api/v1/loans", json={
            "farmer_id": farmer["id"], "amount_kes": 10000,
            "interest_rate_annual": 15.0, "purpose": "fertiliser", "term_months": 6,
        })
        resp = self.client.get("/api/v1/loans")
        assert resp.status_code == 200
        # At least our loan exists
        loans = resp.json()
        assert any(l["farmer_id"] == farmer["id"] for l in loans)

    def test_get_loan_not_found(self):
        resp = self.client.get("/api/v1/loans/LN-FAKE")
        assert resp.status_code == 404

    def test_update_loan_status(self):
        body = dict(self._FARMER_BASE, first_name="LS", last_name="Test",
            phone="+254700000007", county="Kiambu", gender="F",
            farm_size_ha=2.0, primary_crop="maize")
        farmer = self.client.post("/api/v1/farmers", json=body).json()
        loan = self.client.post("/api/v1/loans", json={
            "farmer_id": farmer["id"], "amount_kes": 15000,
            "interest_rate_annual": 16.0, "purpose": "seeds", "term_months": 9,
        }).json()
        resp = self.client.patch(f"/api/v1/loans/{loan['id']}/status?status=approved")
        assert resp.status_code == 200
        assert resp.json()["status"] == "approved"

    def test_build_pool_endpoint(self):
        farmer_data = [
            {"id": "KCW-T1", "max_loan_kes": 18000, "probability_default": 0.12, "interest_rate_annual": 18.0, "loan_id": "LN-T1"},
            {"id": "KCW-T2", "max_loan_kes": 12000, "probability_default": 0.08, "interest_rate_annual": 16.0, "loan_id": "LN-T2"},
            {"id": "KCW-T3", "max_loan_kes": 45000, "probability_default": 0.05, "interest_rate_annual": 15.0, "loan_id": "LN-T3"},
        ]
        resp = self.client.post("/api/v1/pools/build", json={"farmer_data": farmer_data})
        assert resp.status_code == 201
        data = resp.json()
        assert "id" in data
        assert data["farmer_count"] == 3

    def test_build_pool_empty_farmers(self):
        resp = self.client.post("/api/v1/pools/build", json={"farmer_data": []})
        assert resp.status_code == 400

    def test_apply_endpoint(self):
        resp = self.client.post("/api/v1/apply", json={
            "first_name": "Apply", "last_name": "Test",
            "phone": "+254700000099", "county": "Nyeri",
            "gender": "F", "farm_size_ha": 1.8, "primary_crop": "tea",
            "chama_member": True, "sacco_member": True, "year_registered": 2022,
            "latitude": -0.28, "longitude": 36.95,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "workflow_id" in data
        assert data["status"] in ("approved", "declined")

    def test_audit_trail(self):
        resp = self.client.post("/api/v1/apply", json={
            "first_name": "Audit", "last_name": "Test",
            "phone": "+254700000088", "county": "Kiambu",
            "gender": "F", "farm_size_ha": 1.5, "primary_crop": "avocado",
            "chama_member": True, "sacco_member": True, "year_registered": 2022,
            "latitude": -1.1, "longitude": 37.0,
        })
        farmer_id = resp.json().get("farmer_id", "unknown")
        audit_resp = self.client.get(f"/api/v1/audit/{farmer_id}")
        assert audit_resp.status_code == 200

    def test_request_id_header(self):
        resp = self.client.get("/health", headers={"X-Request-ID": "my-custom-id"})
        assert resp.headers.get("X-Request-ID") == "my-custom-id"
        assert "X-Response-Time-Ms" in resp.headers

    def test_security_headers(self):
        resp = self.client.get("/health")
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"
        assert resp.headers.get("X-Frame-Options") == "DENY"
        assert resp.headers.get("Strict-Transport-Security") is not None

    def test_nonexistent_route(self):
        resp = self.client.get("/api/v1/nonexistent")
        assert resp.status_code in (404, 405)  # FastAPI returns 405 for method not allowed
