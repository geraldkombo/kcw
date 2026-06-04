from __future__ import annotations

import logging
from typing import Any, Optional

import httpx

from config.settings import settings

logger = logging.getLogger("frk.google_env")

SOLAR_URL = "https://solar.googleapis.com/v1"


class GoogleEnvironmentClient:
    """Google Solar API client.

    Solar potential data for equatorial agriculture decision-making:
    - Rooftop solar viability for irrigation pumping
    - Solar drying feasibility for post-harvest loss reduction
    - Energy cost savings for agri-processing

    Free tier: 10K calls/month.
    Requires a Google Cloud API key with the Solar API enabled.
    """

    def __init__(self, api_key: str | None = None, timeout: float = 15.0) -> None:
        self._api_key = api_key or settings.google_maps_api_key
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(timeout))

    async def get_solar_potential(self, latitude: float, longitude: float) -> dict[str, Any]:
        if not self._api_key:
            return {"error": "Google Maps API key not configured"}

        try:
            resp = await self._client.get(
                f"{SOLAR_URL}/buildingInsights:findClosest",
                params={
                    "key": self._api_key,
                    "location.latitude": latitude,
                    "location.longitude": longitude,
                    "requiredQuality": "HIGH",
                },
            )
            resp.raise_for_status()
            data = resp.json()

            return {
                "solar_potential": data.get("solarPotential", {}).get("solarPotential", {}),
                "max_installation_panels": data.get("solarPotential", {}).get("maxPanelsCount", 0),
                "roof_summary": data.get("solarPotential", {}).get("roofSegmentStats", []),
            }
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {"error": "no building data found at this location"}
            logger.error("Google Solar API error: %s", e)
            return {"error": "solar API request failed"}
        except Exception as e:
            logger.exception("Google Solar API unexpected error")
            return {"error": str(e)}

    async def close(self):
        await self._client.aclose()
