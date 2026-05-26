from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any, Optional

import httpx

logger = logging.getLogger("kcw.satellite")

POWER_BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

AG_PARAMETERS = [
    "T2M", "T2M_MAX", "T2M_MIN", "PRECTOTCORR",
    "ALLSKY_SFC_SW_DWN", "GWETROOT", "GWETTOP", "RH2M", "WS10M",
]

NASA_FILL = -999.0

CACHE_TTL_SECONDS = 3600  # 1 hour
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0


@dataclass
class CacheEntry:
    data: dict[str, Any]
    expires_at: float


class PowerClient:
    """NASA POWER API client with caching, retry, and circuit breaker."""

    def __init__(self, timeout: float = 30.0) -> None:
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(timeout))
        self._cache: dict[str, CacheEntry] = {}
        self._consecutive_failures = 0
        self._circuit_open = False
        self._circuit_reset_at = 0.0

    def _cache_get(self, key: str) -> Optional[dict[str, Any]]:
        entry = self._cache.get(key)
        if entry and time.monotonic() < entry.expires_at:
            return entry.data
        if entry:
            del self._cache[key]
        return None

    def _cache_set(self, key: str, data: dict[str, Any]) -> None:
        self._cache[key] = CacheEntry(data=data, expires_at=time.monotonic() + CACHE_TTL_SECONDS)

    async def get_ag_point(
        self,
        latitude: float,
        longitude: float,
        start: date | None = None,
        end: date | None = None,
        parameters: list[str] | None = None,
    ) -> dict[str, Any]:
        cache_key = f"{latitude:.2f}_{longitude:.2f}"

        cached = self._cache_get(cache_key)
        if cached is not None:
            return cached

        # Circuit breaker: if too many failures, fail fast
        if self._circuit_open:
            if time.monotonic() < self._circuit_reset_at:
                logger.warning("NASA POWER circuit breaker open, returning empty data")
                return {}
            self._circuit_open = False
            self._consecutive_failures = 0

        if start is None:
            end = end or date.today()
            start = end - timedelta(days=30)
        if end is None:
            end = date.today()

        params = {
            "parameters": ",".join(parameters or AG_PARAMETERS),
            "community": "AG",
            "latitude": latitude,
            "longitude": longitude,
            "start": start.strftime("%Y%m%d"),
            "end": end.strftime("%Y%m%d"),
            "format": "JSON",
        }

        last_exc: Optional[Exception] = None
        for attempt in range(MAX_RETRIES):
            try:
                resp = await self._client.get(POWER_BASE_URL, params=params)
                resp.raise_for_status()
                data = resp.json()
                props = data.get("properties", {})
                self._cache_set(cache_key, props)
                self._consecutive_failures = 0
                return props
            except httpx.TimeoutException as e:
                logger.warning("NASA POWER timeout (attempt %d/%d): %s", attempt + 1, MAX_RETRIES, e)
                last_exc = e
            except httpx.HTTPStatusError as e:
                logger.error("NASA POWER HTTP error (attempt %d/%d): %s", attempt + 1, MAX_RETRIES, e)
                last_exc = e
                if e.response.status_code < 500:
                    break  # Don't retry 4xx errors
            except Exception as e:
                logger.exception("NASA POWER unexpected error (attempt %d/%d)", attempt + 1, MAX_RETRIES)
                last_exc = e

            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_BACKOFF ** attempt)

        # All retries exhausted
        self._consecutive_failures += 1
        if self._consecutive_failures >= 3:
            self._circuit_open = True
            self._circuit_reset_at = time.monotonic() + 300  # 5 min cooldown
            logger.error("NASA POWER circuit breaker opened after %d consecutive failures", self._consecutive_failures)

        logger.error("NASA POWER request failed after %d attempts", MAX_RETRIES)
        return {}

    def _extract_mean(self, props: dict, param: str) -> float | None:
        values = props.get("parameter", {}).get(param, {})
        if isinstance(values, dict):
            vals = [v for v in values.values() if v is not None and v != NASA_FILL]
            if vals:
                return sum(vals) / len(vals)
        return None

    async def get_vegetation_index(self, latitude: float, longitude: float) -> float:
        props = await self.get_ag_point(latitude, longitude)
        if not props:
            return 0.5
        solar = self._extract_mean(props, "ALLSKY_SFC_SW_DWN") or 5.0
        t2m = self._extract_mean(props, "T2M") or 25.0
        t2m_norm = max(0.0, min(1.0, (t2m - 10.0) / 30.0))
        solar_norm = max(0.0, min(1.0, solar / 10.0))
        return round(0.2 + 0.6 * (t2m_norm * 0.4 + solar_norm * 0.6), 4)

    async def get_moisture_stress(self, latitude: float, longitude: float) -> float:
        props = await self.get_ag_point(latitude, longitude)
        if not props:
            return 0.35
        gwetroot = self._extract_mean(props, "GWETROOT")
        prectot = self._extract_mean(props, "PRECTOT")
        if gwetroot is not None:
            stress = 1.0 - gwetroot
            if prectot is not None and prectot < 1.0:
                stress = min(1.0, stress + 0.15)
            return round(stress, 4)
        if prectot is not None:
            return round(max(0.0, min(1.0, 1.0 - prectot / 10.0)), 4)
        return 0.35

    async def get_soil_quality(self, latitude: float, longitude: float) -> str:
        props = await self.get_ag_point(latitude, longitude)
        if not props:
            return "moderate"
        gwetroot = self._extract_mean(props, "GWETROOT")
        t2m = self._extract_mean(props, "T2M")
        if gwetroot is not None and t2m is not None:
            if gwetroot > 0.6 and 15.0 < t2m < 32.0:
                return "good"
            elif gwetroot > 0.3:
                return "moderate"
            else:
                return "poor"
        return "moderate"

    async def get_solar_radiation(self, latitude: float, longitude: float) -> float:
        props = await self.get_ag_point(latitude, longitude)
        if not props:
            return 5.0
        val = self._extract_mean(props, "ALLSKY_SFC_SW_DWN")
        return round(val, 4) if val is not None else 5.0

    async def get_temperature(self, latitude: float, longitude: float) -> dict:
        props = await self.get_ag_point(latitude, longitude)
        if not props:
            return {"mean": 25.0, "max": 32.0, "min": 18.0}
        t2m = self._extract_mean(props, "T2M")
        tmax = self._extract_mean(props, "T2M_MAX")
        tmin = self._extract_mean(props, "T2M_MIN")
        return {
            "mean": round(t2m, 2) if t2m is not None else 25.0,
            "max": round(tmax, 2) if tmax is not None else 32.0,
            "min": round(tmin, 2) if tmin is not None else 18.0,
        }

    async def get_precipitation(self, latitude: float, longitude: float) -> float:
        props = await self.get_ag_point(latitude, longitude)
        if not props:
            return 2.5
        val = self._extract_mean(props, "PRECTOTCORR")
        return round(val, 2) if val is not None else 2.5

    async def close(self):
        await self._client.aclose()
