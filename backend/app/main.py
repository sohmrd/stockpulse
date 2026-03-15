"""FastAPI application factory."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.core.exceptions import AppError, app_error_handler, unhandled_exception_handler

logger = structlog.get_logger()


# ── Lifespan ──────────────────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup / shutdown hooks for the application."""
    # Startup
    logger.info(
        "stockpulse_backend_starting",
        env=settings.APP_ENV,
        version=app.version,
    )

    # TODO: initialise Redis connection pool (Sprint 2)
    # TODO: initialise shared httpx.AsyncClient (Sprint 2)

    yield

    # Shutdown
    logger.info("stockpulse_backend_stopping")


# ── App factory ───────────────────────────────────────────────────────────────


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(
        title="StockPulse API",
        description="AI-Powered Stock Tracking & Insights Platform",
        version="0.1.0",
        docs_url="/docs" if settings.APP_ENV != "production" else None,
        redoc_url="/redoc" if settings.APP_ENV != "production" else None,
        lifespan=lifespan,
    )

    # ── Middleware ─────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Exception handlers ─────────────────────────────────────────────────────
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # ── Routers ────────────────────────────────────────────────────────────────
    app.include_router(v1_router)

    # ── Health check ───────────────────────────────────────────────────────────
    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        return {"status": "ok", "env": settings.APP_ENV}

    return app


app = create_app()
