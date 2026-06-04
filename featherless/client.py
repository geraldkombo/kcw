from __future__ import annotations

from typing import Optional

from config.settings import settings


class FeatherlessClient:
    """Client for Featherless AI — optional LLM augmentation layer."""

    def __init__(self) -> None:
        if not settings.featherless_api_key:
            raise ValueError("FEATHERLESS_API_KEY is not configured")

    async def chat(self, messages: list[dict], **kwargs) -> str:
        return ""

    async def geo_audit(self, context: str) -> dict | str:
        return {}
