from __future__ import annotations

import logging
import time
from collections import defaultdict
from datetime import datetime, timezone

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from config.log import get_request_id, set_request_id
from config.settings import settings

logger = logging.getLogger("kcw.http")


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: ASGIApp) -> Response:
        rid = request.headers.get(settings.request_id_header) or set_request_id()
        set_request_id(rid)
        start = time.monotonic()
        response: Response = await call_next(request)
        elapsed_ms = (time.monotonic() - start) * 1000
        response.headers[settings.request_id_header] = rid
        response.headers["X-Response-Time-Ms"] = f"{elapsed_ms:.1f}"
        logger.info("%s %s -> %d (%.1fms)", request.method, request.url.path, response.status_code, elapsed_ms)
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_per_minute: int = 60) -> None:
        super().__init__(app)
        self.max_per_minute = max_per_minute
        self._buckets: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next: ASGIApp) -> Response:
        if self.max_per_minute <= 0:
            return await call_next(request)
        client_ip = request.client.host if request.client else "unknown"
        now = time.monotonic()
        window = 60.0
        bucket = self._buckets[client_ip]
        bucket[:] = [t for t in bucket if now - t < window]
        if len(bucket) >= self.max_per_minute:
            logger.warning("rate limit exceeded for %s", client_ip)
            return JSONResponse(
                status_code=429,
                content={
                    "error": "rate_limit_exceeded",
                    "message": f"Max {self.max_per_minute} requests per minute",
                    "retry_after_seconds": int(window - (now - bucket[0])),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
                headers={"Retry-After": str(int(window - (now - bucket[0])))},
            )
        bucket.append(now)
        return await call_next(request)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: ASGIApp) -> Response:
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Cache-Control"] = "no-store"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response


class APIKeyMiddleware(BaseHTTPMiddleware):
    """Enforces Bearer token authentication on all endpoints except public probes.
    In production, API_KEY must be set - startup will fail if unset."""

    PUBLIC_PATHS = {"/health", "/ready", "/docs", "/openapi.json", "/redoc", "/"}

    async def dispatch(self, request: Request, call_next: ASGIApp) -> Response:
        if request.url.path in self.PUBLIC_PATHS:
            return await call_next(request)

        auth = request.headers.get("Authorization", "")

        if settings.api_key and auth == f"Bearer {settings.api_key}":
            return await call_next(request)
        if not settings.api_key:
            logger.warning("API authentication is DISABLED - set API_KEY env var in production")
            return await call_next(request)

        logger.warning("unauthorized request to %s from %s", request.url.path, request.client.host if request.client else "unknown")
        return JSONResponse(
            status_code=401,
            content={
                "error": "unauthorized",
                "message": "Missing or invalid API key. Provide Authorization: Bearer <key>",
                "request_id": get_request_id(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: ASGIApp) -> Response:
        try:
            response: Response = await call_next(request)
            if response.status_code >= 500:
                logger.error("server error %d on %s %s", response.status_code, request.method, request.url.path)
            return response
        except Exception as exc:
            logger.exception("unhandled exception on %s %s", request.method, request.url.path)
            return JSONResponse(
                status_code=500,
                content={
                    "error": "internal_error",
                    "message": "An unexpected error occurred",
                    "request_id": get_request_id(),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )


class RequestBodySizeMiddleware(BaseHTTPMiddleware):
    """Enforce maximum request body size (default 10MB)."""

    def __init__(self, app: ASGIApp, max_size_bytes: int = 10 * 1024 * 1024) -> None:
        super().__init__(app)
        self.max_size_bytes = max_size_bytes

    async def dispatch(self, request: Request, call_next: ASGIApp) -> Response:
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_size_bytes:
            return JSONResponse(
                status_code=413,
                content={
                    "error": "request_too_large",
                    "message": f"Request body exceeds {self.max_size_bytes // (1024*1024)}MB limit",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )
        return await call_next(request)


def register_middleware(app: FastAPI) -> None:
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(
        RateLimitMiddleware,
        max_per_minute=settings.rate_limit_per_minute,
    )
    app.add_middleware(RequestBodySizeMiddleware, max_size_bytes=settings.request_max_body_mb * 1024 * 1024)
    app.add_middleware(APIKeyMiddleware)
    app.add_middleware(RequestIDMiddleware)
