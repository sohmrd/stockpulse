"""Aggregates all v1 API routers under the /api/v1 prefix."""

from fastapi import APIRouter

from app.api.v1 import alerts, auth, insights, portfolio, stocks, watchlist

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(stocks.router)
router.include_router(portfolio.router)
router.include_router(watchlist.router)
router.include_router(insights.router)
router.include_router(alerts.router)
