import uuid
from typing import Optional

from featherless.client import FeatherlessClient


class OnboardingAgent:
    """Farmer Interface Agent — ingests NL farmer data, M-Pesa velocity,
    geolocation, and chama/SACCO membership.
    """

    def __init__(self, featherless: Optional[FeatherlessClient] = None):
        self.featherless = featherless

    async def ingest(self, raw: dict) -> dict:
        farmer_id = raw.get("id", f"KCW-{uuid.uuid4().hex[:8].upper()}")

        profile = {
            "id": farmer_id,
            "first_name": raw.get("first_name", ""),
            "last_name": raw.get("last_name", ""),
            "phone": raw.get("phone", ""),
            "gender": raw.get("gender", "M"),
            "county": raw.get("county", ""),
            "sub_county": raw.get("sub_county", ""),
            "village": raw.get("village", ""),
            "latitude": raw.get("latitude", 0.0),
            "longitude": raw.get("longitude", 0.0),
            "farm_size_ha": raw.get("farm_size_ha", 1.0),
            "primary_crop": raw.get("primary_crop", "maize"),
            "year_registered": raw.get("year_registered", 2025),
            "chama_member": raw.get("chama_member", False),
            "sacco_member": raw.get("sacco_member", False),
            "has_mpesa_account": raw.get("has_mpesa_account", True),
            "mpesa_monthly_velocity": raw.get("mpesa_monthly_velocity", 0),
            "source_language": raw.get("source_language", "en"),
        }

        # If NL text provided, parse via Gemma 4 (multilingual)
        if raw.get("raw_text") and self.featherless:
            parsed = await self.featherless.multilingual_parse(raw["raw_text"])
            if isinstance(parsed, str):
                import json
                try:
                    parsed = json.loads(parsed)
                except json.JSONDecodeError:
                    pass
            if isinstance(parsed, dict):
                profile.update(parsed)

        return profile
