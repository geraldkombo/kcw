from __future__ import annotations

from database.repository import Repository, create_repository
from featherless.client import FeatherlessClient
from satellite.google_environment_client import GoogleEnvironmentClient
from satellite.openmeteo_client import OpenMeteoClient
from satellite.power_client import PowerClient

_featherless: FeatherlessClient | None = None
_power: PowerClient | None = None
_openmeteo: OpenMeteoClient | None = None
_google_env: GoogleEnvironmentClient | None = None
_repository: Repository | None = None


def get_featherless() -> FeatherlessClient | None:
    global _featherless
    if _featherless is None:
        try:
            _featherless = FeatherlessClient()
        except ValueError:
            _featherless = None
    return _featherless


def get_power() -> PowerClient:
    global _power
    if _power is None:
        _power = PowerClient()
    return _power


def get_openmeteo() -> OpenMeteoClient:
    global _openmeteo
    if _openmeteo is None:
        _openmeteo = OpenMeteoClient()
    return _openmeteo


def get_google_environment() -> GoogleEnvironmentClient:
    global _google_env
    if _google_env is None:
        _google_env = GoogleEnvironmentClient()
    return _google_env


def get_repository() -> Repository:
    global _repository
    if _repository is None:
        _repository = create_repository()
    return _repository
