from __future__ import annotations

import pytest

from satellite.openmeteo_client import OpenMeteoClient


@pytest.fixture
def client():
    return OpenMeteoClient(timeout=10.0)


@pytest.mark.asyncio
async def test_forecast_returns_data(client: OpenMeteoClient):
    data = await client.get_forecast(-1.0, 36.8, days=3)
    assert "daily" in data
    daily = data["daily"]
    assert "temperature_2m_max" in daily
    assert "precipitation_sum" in daily


@pytest.mark.asyncio
async def test_forecast_temperature(client: OpenMeteoClient):
    result = await client.get_temperature_forecast(-1.0, 36.8)
    assert "max" in result
    assert "min" in result


@pytest.mark.asyncio
async def test_forecast_precipitation(client: OpenMeteoClient):
    result = await client.get_precipitation_forecast(-1.0, 36.8)
    assert "total" in result
    assert "max_daily" in result
    assert "rain_days" in result


@pytest.mark.asyncio
async def test_forecast_humidity(client: OpenMeteoClient):
    result = await client.get_humidity_forecast(-1.0, 36.8)
    assert 0 <= result <= 100


@pytest.mark.asyncio
async def test_forecast_wind(client: OpenMeteoClient):
    result = await client.get_wind_speed_forecast(-1.0, 36.8)
    assert result >= 0


@pytest.mark.asyncio
async def test_cache_hits(client: OpenMeteoClient):
    result1 = await client.get_forecast(-1.0, 36.8, days=3)
    result2 = await client.get_forecast(-1.0, 36.8, days=3)
    assert result1 == result2


@pytest.mark.asyncio
async def test_different_coordinates_different_cache(client: OpenMeteoClient):
    result1 = await client.get_forecast(-1.0, 36.8, days=3)
    result2 = await client.get_forecast(0.05, 34.7, days=3)
    assert result1 != result2
