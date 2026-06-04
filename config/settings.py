from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )

    # Database
    database_url: str = Field(default="sqlite:///data/frk.db")
    neo4j_uri: str = Field(default="bolt://localhost:7687")
    neo4j_user: str = Field(default="neo4j")
    neo4j_password: str = Field(default="")

    # App
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000, ge=1024, le=65535)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(default="INFO")
    log_json: bool = Field(default=True)
    cors_origins: str = Field(default="*")
    rate_limit_per_minute: int = Field(default=60, ge=0)
    api_key: str | None = Field(default=None)
    request_id_header: str = Field(default="X-Request-ID")
    request_max_body_mb: int = Field(default=10, ge=1, le=100)

    # Featherless AI (optional LLM augmentation)
    featherless_api_key: str | None = Field(default=None)
    featherless_base_url: str = Field(default="https://api.featherless.ai/v1")
    featherless_model: str = Field(default="meta-llama/llama-3.1-8b-instruct")

    # Masumi x402 (decentralised micropayments)
    masumi_api_url: str = Field(default="https://payment-service.masumi.network")
    masumi_wallet_address: str = Field(default="")
    masumi_wallet_mnemonic: str = Field(default="")

    # Google Maps Platform (Solar API)
    google_maps_api_key: str | None = Field(default=None)

    # Data
    data_dir: Path = Field(default=Path("data"))

    @field_validator("neo4j_uri")
    @classmethod
    def validate_neo4j_uri(cls, v: str) -> str:
        if v and not v.startswith("bolt://") and not v.startswith("neo4j://") and not v.startswith("neo4j+s://"):
            raise ValueError("NEO4J_URI must start with bolt://, neo4j://, or neo4j+s://")
        return v

    @model_validator(mode="after")
    def parse_cors(self) -> "Settings":
        if isinstance(self.cors_origins, str):
            origins = [o.strip() for o in self.cors_origins.split(",") if o.strip()]
            object.__setattr__(self, "_cors_origins_list", origins)
        else:
            object.__setattr__(self, "_cors_origins_list", ["*"])
        return self

    @property
    def cors_origins_list(self) -> list[str]:
        return getattr(self, "_cors_origins_list", ["*"])


settings = Settings()


def validate_settings() -> list[str]:
    warnings = []
    if settings.api_key is None:
        warnings.append("API_KEY is not set — API authentication is DISABLED (set API_KEY env var for production)")
    if settings.neo4j_password == "" and settings.database_url.startswith("neo4j"):
        warnings.append("NEO4J_PASSWORD is empty — set a strong password for production")
    if settings.cors_origins == "*":
        warnings.append("CORS_ORIGINS=* — restrict this to specific origins in production")
    if settings.database_url.startswith("sqlite"):
        db_path = settings.database_url.replace("sqlite:///", "")
        warnings.append(f"Using SQLite ({db_path}) — data persists to disk but consider PostgreSQL for multi-instance deployment")
    if settings.featherless_api_key is None:
        warnings.append("FEATHERLESS_API_KEY is not set — LLM augmentation disabled (graceful degradation)")
    return warnings
