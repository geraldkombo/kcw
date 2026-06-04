from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from api.middleware import register_middleware
from api.routes.agriculture_intelligence import router as agri_intel_router
from api.routes.weather import router as weather_router
from api.routes.rag import router as rag_router
from api.routes.traditional_foods import router as traditional_foods_router
from api.routes.marketplace import router as marketplace_router
from api.routes.climate_finance import router as climate_finance_router
from api.dependencies import get_repository
from config.log import configure_logging
from config.settings import settings, validate_settings
from database.repository import Repository

logger = logging.getLogger("frk")

_start_time: datetime = datetime.now(timezone.utc)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings.log_level, settings.log_json)
    for w in validate_settings():
        logger.warning("startup warning: %s", w)

    repo = get_repository()
    await repo.connect()

    db_type = type(repo).__name__.replace("Repository", "")
    logger.info(
        "starting Food Roots KE v1.0.0",
        extra={
            "database": f"{db_type} (connected: {repo.connected})",
            "api_key": "set" if settings.api_key else "not set (open access)",
            "rate_limit": f"{settings.rate_limit_per_minute}/min",
            "log_json": settings.log_json,
        },
    )

    yield

    logger.info("shutting down Food Roots KE")
    repo = get_repository()
    await repo.disconnect()


app = FastAPI(
    title="Food Roots KE API",
    description="Traditional food plants intelligence system for Kenya",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_middleware(app)

app.include_router(agri_intel_router)
app.include_router(weather_router)
app.include_router(rag_router)
app.include_router(traditional_foods_router)
app.include_router(marketplace_router)
app.include_router(climate_finance_router)


@app.get("/health")
async def health(repo: Repository = Depends(get_repository)):
    return {
        "status": "ok",
        "service": "food-roots-ke",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": type(repo).__name__.replace("Repository", ""),
        "database_connected": repo.connected,
        "uptime_seconds": (datetime.now(timezone.utc) - _start_time).total_seconds(),
    }


@app.get("/ready")
async def ready(repo: Repository = Depends(get_repository)):
    from fastapi.responses import JSONResponse
    if not repo.connected:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "database": "disconnected",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )
    return {
        "status": "ready",
        "database": "connected",
        "database_type": type(repo).__name__.replace("Repository", ""),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


class ConfigStatus(BaseModel):
    neo4j_uri: str
    database_type: str
    api_key_set: bool
    rate_limit_per_minute: int
    cors_origins: str
    log_json: bool
    log_level: str


@app.get("/api/v1/config", response_model=ConfigStatus)
async def get_config(repo: Repository = Depends(get_repository)):
    return ConfigStatus(
        neo4j_uri=settings.neo4j_uri,
        database_type=type(repo).__name__.replace("Repository", ""),
        api_key_set=settings.api_key is not None,
        rate_limit_per_minute=settings.rate_limit_per_minute,
        cors_origins=settings.cors_origins,
        log_json=settings.log_json,
        log_level=settings.log_level,
    )
