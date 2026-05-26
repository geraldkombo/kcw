import os
import httpx
from typing import Optional


FEATHERLESS_BASE_URL = "https://api.featherless.ai/v1"


class FeatherlessClient:
    """Pay-as-you-go Featherless API client for model access.
    Uses FEATHERLESS_API_KEY env var. No flat fee required.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("FEATHERLESS_API_KEY")
        if not self.api_key:
            raise ValueError(
                "FEATHERLESS_API_KEY required. Set in .env or pass directly."
            )
        self._client = httpx.AsyncClient(
            base_url=FEATHERLESS_BASE_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=60.0,
        )

    async def close(self):
        await self._client.aclose()

    async def chat_completion(
        self,
        model: str,
        messages: list[dict],
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> dict:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        resp = await self._client.post("/chat/completions", json=payload)
        resp.raise_for_status()
        return resp.json()

    # ---- Convenience methods for KCW agent models ----

    async def credit_assessment(
        self, farmer_data: dict, prompt: str
    ) -> str:
        """DeepSeek V4 Pro (862B, Apr 2026) for credit reasoning."""
        messages = [
            {
                "role": "system",
                "content": "You are a credit assessment agent for Kilimo Credit Web. "
                "Analyse smallholder farmer data and return a structured credit assessment. "
                "Output JSON with: probability_default, credit_score, risk_factors[], reasoning.",
            },
            {"role": "user", "content": f"Farmer data:\n{farmer_data}\n\n{prompt}"},
        ]
        result = await self.chat_completion(
            model="deepseek/deepseek-v4-pro", messages=messages
        )
        return result["choices"][0]["message"]["content"]

    async def multilingual_parse(
        self, text: str, source_lang: str = "sw"
    ) -> dict:
        """Gemma 4 (31B, Mar 2026) for Swahili/vernacular farmer input."""
        messages = [
            {
                "role": "system",
                "content": "You are an agricultural intake agent. Parse farmer messages "
                "in Swahili/sheng/English into structured JSON with fields: "
                "intent, crop, location, amount_requested, language.",
            },
            {"role": "user", "content": text},
        ]
        result = await self.chat_completion(
            model="google/gemma-4-27b-it", messages=messages
        )
        return result["choices"][0]["message"]["content"]

    async def geo_audit(self, satellite_context: str) -> str:
        """MiniMax M2.5 (default Featherless model) for geo-spatial analysis."""
        messages = [
            {
                "role": "system",
                "content": "Analyse satellite/geospatial data and assess agricultural "
                "conditions. Output JSON with: vegetation_index, moisture_stress, "
                "drought_risk, recommended_crops.",
            },
            {"role": "user", "content": satellite_context},
        ]
        result = await self.chat_completion(
            model="minimax/minimax-m2.5", messages=messages
        )
        return result["choices"][0]["message"]["content"]
