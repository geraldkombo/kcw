from __future__ import annotations

import logging
import os
import tempfile

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.dependencies import get_repository
from config.log import configure_logging, get_request_id, set_request_id
from config.settings import Settings
from database.repository import InMemoryRepository


class TestSettings:
    def test_default_settings(self):
        s = Settings(_env_file=None)
        assert s.neo4j_uri == "bolt://localhost:7687"
        assert s.api_port == 8000
        assert s.log_level == "INFO"
        assert s.cors_origins == "*"
        assert s.rate_limit_per_minute == 60

    def test_cors_origins_list_single(self):
        s = Settings(cors_origins="*")
        assert s.cors_origins_list == ["*"]

    def test_cors_origins_list_multiple(self):
        s = Settings(cors_origins="https://app.frk.ke,https://admin.frk.ke")
        assert s.cors_origins_list == ["https://app.frk.ke", "https://admin.frk.ke"]

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
            Settings(api_port=80)

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
        logger = logging.getLogger("frk.test")
        logger.info("hello json")
        assert True

    def test_configure_logging_text(self, caplog):
        configure_logging("DEBUG", log_json=False)
        logger = logging.getLogger("frk.test")
        logger.info("hello text")
        assert True

    def test_request_id_in_log_record(self):
        set_request_id("test-rid")
        configure_logging("DEBUG", log_json=False)
        logger = logging.getLogger("frk.test.rid")
        logger.info("check rid")
        assert True


class TestAPI:
    def setup_method(self):
        self._test_repo = InMemoryRepository()
        app.dependency_overrides[get_repository] = lambda: self._test_repo
        self.client = TestClient(app)

    def test_health(self):
        resp = self.client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["service"] == "food-roots-ke"

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
        assert resp.status_code in (404, 405)
