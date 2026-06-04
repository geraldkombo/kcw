from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any, Optional

import httpx

logger = logging.getLogger("frk.openmeteo")

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
ERA5_URL = "https://archive-api.open-meteo.com/v1/era5"

CACHE_TTL_SECONDS = 1800
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

FORECAST_PARAMS = [
    "temperature_2m_max", "temperature_2m_min",
    "precipitation_sum",
    "wind_speed_10m_max",
    "relative_humidity_2m_max",
]

ERA5_PARAMS = [
    "temperature_2m_max", "temperature_2m_min",
    "precipitation_sum",
]


@dataclass
class CacheEntry:
    data: dict[str, Any]
    expires_at: float


class OpenMeteoClient:
    """Open-Meteo weather API client (free, no key, 10K calls/day).

    Complements NASA POWER by providing:
    - 7-day forecast (NASA POWER is historical only)
    - ERA5 reanalysis back to 1940
    - Higher temporal resolution (hourly)
    """

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

    async def get_forecast(
        self,
        latitude: float,
        longitude: float,
        days: int = 7,
    ) -> dict[str, Any]:
        cache_key = f"forecast_{latitude:.2f}_{longitude:.2f}_{days}"
        cached = self._cache_get(cache_key)
        if cached is not None:
            return cached

        if self._circuit_open:
            if time.monotonic() < self._circuit_reset_at:
                logger.warning("Open-Meteo circuit breaker open, returning empty data")
                return {}
            self._circuit_open = False
            self._consecutive_failures = 0

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": ",".join(FORECAST_PARAMS),
            "forecast_days": min(days, 16),
            "timezone": "Africa/Nairobi",
        }

        return await self._request(FORECAST_URL, params, cache_key)

    async def get_era5(
        self,
        latitude: float,
        longitude: float,
        start: date | None = None,
        end: date | None = None,
    ) -> dict[str, Any]:
        if end is None:
            end = date.today() - timedelta(days=5)
        if start is None:
            start = end - timedelta(days=30)

        cache_key = f"era5_{latitude:.2f}_{longitude:.2f}_{start}_{end}"
        cached = self._cache_get(cache_key)
        if cached is not None:
            return cached

        if self._circuit_open:
            if time.monotonic() < self._circuit_reset_at:
                logger.warning("Open-Meteo ERA5 circuit breaker open, returning empty data")
                return {}
            self._circuit_open = False
            self._consecutive_failures = 0

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start.strftime("%Y-%m-%d"),
            "end_date": end.strftime("%Y-%m-%d"),
            "daily": ",".join(ERA5_PARAMS),
            "timezone": "Africa/Nairobi",
        }

        return await self._request(ERA5_URL, params, cache_key)

    async def _request(self, url: str, params: dict, cache_key: str) -> dict[str, Any]:
        last_exc: Optional[Exception] = None
        for attempt in range(MAX_RETRIES):
            try:
                resp = await self._client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()
                self._cache_set(cache_key, data)
                self._consecutive_failures = 0
                return data
            except httpx.TimeoutException as e:
                logger.warning("Open-Meteo timeout (attempt %d/%d): %s", attempt + 1, MAX_RETRIES, e)
                last_exc = e
            except httpx.HTTPStatusError as e:
                logger.error("Open-Meteo HTTP error (attempt %d/%d): %s", attempt + 1, MAX_RETRIES, e)
                last_exc = e
                if e.response.status_code < 500:
                    break
            except Exception as e:
                logger.exception("Open-Meteo unexpected error (attempt %d/%d)", attempt + 1, MAX_RETRIES)
                last_exc = e

            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_BACKOFF ** attempt)

        self._consecutive_failures += 1
        if self._consecutive_failures >= 3:
            self._circuit_open = True
            self._circuit_reset_at = time.monotonic() + 300
            logger.error("Open-Meteo circuit breaker opened after %d consecutive failures", self._consecutive_failures)

        logger.error("Open-Meteo request failed after %d attempts", MAX_RETRIES)
        return {}

    async def get_temperature_forecast(self, latitude: float, longitude: float) -> dict:
        data = await self.get_forecast(latitude, longitude)
        daily = data.get("daily", {})
        tmax = daily.get("temperature_2m_max", [])
        tmin = daily.get("temperature_2m_min", [])
        if tmax:
            mean_max = sum(tmax) / len(tmax)
            return {
                "max": round(max(tmax), 1),
                "min": round(min(tmin), 1) if tmin else None,
                "mean_high": round(mean_max, 1),
            }
        return {"max": 32.0, "min": 18.0, "mean_high": 25.0}

    async def get_precipitation_forecast(self, latitude: float, longitude: float) -> dict:
        data = await self.get_forecast(latitude, longitude)
        daily = data.get("daily", {})
        precip = daily.get("precipitation_sum", [])
        if precip:
            return {
                "total": round(sum(precip), 1),
                "max_daily": round(max(precip), 1),
                "rain_days": sum(1 for p in precip if p > 0.1),
            }
        return {"total": 0.0, "max_daily": 0.0, "rain_days": 0}

    async def get_humidity_forecast(self, latitude: float, longitude: float) -> float:
        data = await self.get_forecast(latitude, longitude)
        daily = data.get("daily", {})
        humidity = daily.get("relative_humidity_2m_max", [])
        if humidity:
            return round(sum(humidity) / len(humidity), 1)
        return 65.0

    async def get_wind_speed_forecast(self, latitude: float, longitude: float) -> float:
        data = await self.get_forecast(latitude, longitude)
        daily = data.get("daily", {})
        wind = daily.get("wind_speed_10m_max", [])
        if wind:
            return round(sum(wind) / len(wind), 1)
        return 3.0

    async def close(self):
        await self._client.aclose()
