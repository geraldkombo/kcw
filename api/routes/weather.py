from __future__ import annotations

from fastapi import APIRouter, Depends

from api.dependencies import get_google_environment, get_openmeteo
from satellite.google_environment_client import GoogleEnvironmentClient
from satellite.openmeteo_client import OpenMeteoClient

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/forecast")
async def forecast(
    latitude: float,
    longitude: float,
    days: int = 7,
    client: OpenMeteoClient = Depends(get_openmeteo),
):
    temp = await client.get_temperature_forecast(latitude, longitude)
    precip = await client.get_precipitation_forecast(latitude, longitude)
    humidity = await client.get_humidity_forecast(latitude, longitude)
    wind = await client.get_wind_speed_forecast(latitude, longitude)
    return {
        "source": "open-meteo",
        "latitude": latitude,
        "longitude": longitude,
        "forecast_days": days,
        "temperature": temp,
        "precipitation": precip,
        "humidity": humidity,
        "wind_speed": wind,
    }


@router.get("/forecast/temperature")
async def forecast_temperature(
    latitude: float,
    longitude: float,
    client: OpenMeteoClient = Depends(get_openmeteo),
):
    return await client.get_temperature_forecast(latitude, longitude)


@router.get("/forecast/precipitation")
async def forecast_precipitation(
    latitude: float,
    longitude: float,
    client: OpenMeteoClient = Depends(get_openmeteo),
):
    return await client.get_precipitation_forecast(latitude, longitude)


@router.get("/forecast/humidity")
async def forecast_humidity(
    latitude: float,
    longitude: float,
    client: OpenMeteoClient = Depends(get_openmeteo),
):
    return await client.get_humidity_forecast(latitude, longitude)


@router.get("/forecast/wind")
async def forecast_wind(
    latitude: float,
    longitude: float,
    client: OpenMeteoClient = Depends(get_openmeteo),
):
    return await client.get_wind_speed_forecast(latitude, longitude)


@router.get("/reanalysis")
async def reanalysis(
    latitude: float,
    longitude: float,
    client: OpenMeteoClient = Depends(get_openmeteo),
):
    return await client.get_era5(latitude, longitude)


@router.get("/environment/solar")
async def solar_potential(
    latitude: float,
    longitude: float,
    client: GoogleEnvironmentClient = Depends(get_google_environment),
):
    return await client.get_solar_potential(latitude, longitude)
