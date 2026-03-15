"""Market data service — fetches quotes and historical prices from the configured provider."""

from __future__ import annotations

import structlog

from app.core.config import settings
from app.schemas.stock import StockHistory, StockQuote, StockSearchResult

logger = structlog.get_logger()


class MarketService:
    """Wraps market data API calls with caching and retry.

    TODO (Sprint 2): implement httpx calls, Redis caching, and tenacity retry.
    """

    def __init__(self) -> None:
        self.provider = settings.MARKET_DATA_PROVIDER

    async def search(self, query: str) -> list[StockSearchResult]:
        """Search for stocks by keyword or ticker.

        TODO (Sprint 2): call Alpha Vantage / Polygon / Finnhub search endpoint.
        """
        logger.info("market_search", query=query, provider=self.provider)
        return []

    async def get_quote(self, ticker: str) -> StockQuote:
        """Fetch the latest quote for *ticker*.

        TODO (Sprint 2): implement with caching (TTL=30s).
        Raises ``NotFoundError`` if ticker is unknown.
        """
        logger.info("market_quote", ticker=ticker, provider=self.provider)
        raise NotImplementedError("MarketService.get_quote is not yet implemented.")

    async def get_history(self, ticker: str, time_range: str) -> StockHistory:
        """Fetch OHLCV history for *ticker* over *time_range*.

        TODO (Sprint 2): map time_range to provider interval/outputsize params.
        """
        logger.info("market_history", ticker=ticker, time_range=time_range)
        raise NotImplementedError("MarketService.get_history is not yet implemented.")
