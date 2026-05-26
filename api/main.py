from __future__ import annotations

import asyncio
import logging
import signal
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from api.middleware import register_middleware
from api.routes.farmers import router as farmers_router
from api.routes.loans import router as loans_router
from api.routes.securitisation import router as securitisation_router
from api.routes.payments import router as payments_router
from api.routes.agriculture_intelligence import router as agri_intel_router
from api.dependencies import get_audit, get_masumi, get_orchestrator, get_securitisation, get_repository
from config.log import configure_logging
from config.settings import settings, validate_settings
from database.repository import Repository

logger = logging.getLogger("kcw")

shutdown_event = asyncio.Event()
_start_time: datetime = datetime.now(timezone.utc)


async def _shutdown():
    logger.info("received shutdown signal")
    shutdown_event.set()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings.log_level, settings.log_json)
    for w in validate_settings():
        logger.warning("startup warning: %s", w)

    repo = get_repository()
    await repo.connect()

    db_type = type(repo).__name__.replace("Repository", "")
    logger.info(
        "starting Kilimo Credit Web v1.0.0",
        extra={
            "database": f"{db_type} (connected: {repo.connected})",
            "featherless": "configured" if settings.featherless_api_key else "not configured",
            "api_key": "set" if settings.api_key else "not set (open access)",
            "rate_limit": f"{settings.rate_limit_per_minute}/min",
            "log_json": settings.log_json,
        },
    )

    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        try:
            loop.add_signal_handler(sig, lambda: asyncio.create_task(_shutdown()))
        except NotImplementedError:
            pass

    yield

    logger.info("shutting down Kilimo Credit Web")
    repo = get_repository()
    await repo.disconnect()


app = FastAPI(
    title="Kilimo Credit Web API",
    description="Decentralised AI-agent infrastructure for smallholder agricultural securitisation",
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

app.include_router(farmers_router, prefix="/api/v1/farmers", tags=["Farmers"])
app.include_router(loans_router, prefix="/api/v1/loans", tags=["Loans"])
app.include_router(securitisation_router, prefix="/api/v1/pools", tags=["Securitisation"])
app.include_router(payments_router, prefix="/api/v1/payments", tags=["Payments"])
app.include_router(agri_intel_router)


@app.get("/health")
async def health(repo: Repository = Depends(get_repository)):
    return {
        "status": "ok",
        "service": "kilimo-credit-web",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": type(repo).__name__.replace("Repository", ""),
        "database_connected": repo.connected,
        "uptime_seconds": (datetime.now(timezone.utc) - _start_time).total_seconds(),
    }


@app.get("/ready")
async def ready(repo: Repository = Depends(get_repository)):
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


@app.post("/api/v1/apply")
async def apply(application: dict, repo: Repository = Depends(get_repository)):
    orchestrator = get_orchestrator()
    result = await orchestrator.process_farmer_application(application)
    repo.record_audit({
        "event_type": "loan_application",
        "actor": "farmer",
        "farmer_id": result.get("farmer_id", "unknown"),
        "data": result,
    })
    return result


@app.get("/api/v1/audit/{farmer_id}")
async def get_audit_trail(farmer_id: str, repo: Repository = Depends(get_repository)):
    return repo.get_audit(farmer_id)


@app.get("/api/v1/audit")
async def get_all_audit(repo: Repository = Depends(get_repository)):
    return repo.get_all_audit()


class ConfigStatus(BaseModel):
    neo4j_uri: str
    database_type: str
    featherless_configured: bool
    masumi_configured: bool
    api_key_set: bool
    rate_limit_per_minute: int
    cors_origins: str
    log_json: bool
    log_level: str
    securitisation_min_pool_size: int
    securitisation_target_rating: str
    default_currency: str


@app.get("/api/v1/config", response_model=ConfigStatus)
async def get_config(repo: Repository = Depends(get_repository)):
    return ConfigStatus(
        neo4j_uri=settings.neo4j_uri,
        database_type=type(repo).__name__.replace("Repository", ""),
        featherless_configured=settings.featherless_api_key is not None,
        masumi_configured=bool(settings.masumi_wallet_address and settings.usdm_contract_addr),
        api_key_set=settings.api_key is not None,
        rate_limit_per_minute=settings.rate_limit_per_minute,
        cors_origins=settings.cors_origins,
        log_json=settings.log_json,
        log_level=settings.log_level,
        securitisation_min_pool_size=settings.securitisation_min_pool_size,
        securitisation_target_rating=settings.securitisation_target_rating,
        default_currency=settings.default_currency,
    )
