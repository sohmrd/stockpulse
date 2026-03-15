"""Market data service — fetches quotes and historical prices from the Finnhub API."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal

import httpx
import structlog
from cachetools import TTLCache
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.exceptions import ExternalServiceError, NotFoundError, RateLimitError, UnauthorizedError
from app.schemas.stock import PricePoint, StockHistory, StockQuote, StockSearchResult

logger = structlog.get_logger()

_FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

# ── Resolution / time-range mapping ───────────────────────────────────────────

_RESOLUTION_MAP: dict[str, str] = {
    "1D": "D",
    "1W": "D",
    "1M": "D",
    "3M": "M",
    "6M": "M",
    "1Y": "M",
    "5Y": "M",
}

_TIMEDELTA_MAP: dict[str, timedelta] = {
    "1D": timedelta(days=1),
    "1W": timedelta(weeks=1),
    "1M": timedelta(days=30),
    "3M": timedelta(days=90),
    "6M": timedelta(days=180),
    "1Y": timedelta(days=365),
    "5Y": timedelta(days=365 * 5),
}

# ── In-memory TTL caches (module-level singletons) ────────────────────────────
# Module-level so the cache survives across request-scoped MarketService instances.

_quote_cache: TTLCache[str, StockQuote] = TTLCache(maxsize=512, ttl=30)
_search_cache: TTLCache[str, list[StockSearchResult]] = TTLCache(maxsize=256, ttl=300)
_history_cache: TTLCache[str, StockHistory] = TTLCache(maxsize=256, ttl=300)


class MarketService:
    """Wraps Finnhub API calls with in-memory TTL caching and tenacity retry."""

    def __init__(self) -> None:
        self.provider = settings.MARKET_DATA_PROVIDER
        self._api_key = settings.MARKET_DATA_API_KEY
        self._client = httpx.AsyncClient(
            base_url=_FINNHUB_BASE_URL,
            timeout=10.0,
        )

    async def close(self) -> None:
        """Close the underlying httpx client. Called by the FastAPI dependency on teardown."""
        await self._client.aclose()

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _auth_params(self) -> dict[str, str]:
        return {"token": self._api_key}

    @retry(
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TimeoutException)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=10),
        reraise=True,
    )
    async def _get(self, path: str, params: dict[str, str | int]) -> dict[str, object]:
        """Execute a GET request against Finnhub with retry on 5xx errors and timeouts.

        - HTTP 429 raises ``RateLimitError`` immediately (no retry).
        - HTTP 403 raises ``UnauthorizedError`` immediately (bad API key).
        - HTTP 5xx raises ``httpx.HTTPStatusError`` so tenacity retries up to 3 times.
        - Other 4xx raises ``ExternalServiceError`` immediately.
        """
        all_params: dict[str, str | int] = {**params, **self._auth_params()}
        try:
            response = await self._client.get(path, params=all_params)
        except httpx.TimeoutException:
            logger.warning("finnhub_timeout", path=path)
            raise  # tenacity will retry

        if response.status_code == 429:
            retry_after_header = response.headers.get("Retry-After", "60")
            try:
                retry_after = int(retry_after_header)
            except ValueError:
                retry_after = 60
            raise RateLimitError(retry_after)

        if response.status_code == 403:
            raise UnauthorizedError("Finnhub API key is invalid or missing")

        if response.status_code >= 500:
            # Raise HTTPStatusError so tenacity's retry_if_exception_type picks it up.
            raise httpx.HTTPStatusError(
                message=f"Finnhub server error {response.status_code}",
                request=response.request,
                response=response,
            )

        if not response.is_success:
            raise ExternalServiceError("finnhub", f"HTTP {response.status_code}")

        return response.json()  # type: ignore[no-any-return]

    # ── Public API ────────────────────────────────────────────────────────────

    async def search(self, query: str) -> list[StockSearchResult]:
        """Search for stocks by keyword or ticker symbol.

        Results are cached for 300 seconds.
        Raises ``NotFoundError`` when Finnhub returns no matching symbols.
        """
        cache_key = f"search:{query.lower()}"
        cached = _search_cache.get(cache_key)
        if cached is not None:
            logger.info("market_search", query=query, provider=self.provider, cache_hit=True)
            return cached

        logger.info("market_search", query=query, provider=self.provider, cache_hit=False)

        data = await self._get("/search", {"q": query})

        raw_results: list[dict[str, str]] = data.get("result") or []  # type: ignore[assignment]

        if not raw_results:
            raise NotFoundError("Stock", query)

        results = [
            StockSearchResult(
                ticker=item.get("symbol", ""),
                name=item.get("description", ""),
                exchange=item.get("displaySymbol", ""),
                asset_type=item.get("type", "Equity") or "Equity",
            )
            for item in raw_results
            if item.get("symbol")
        ]

        _search_cache[cache_key] = results
        return results

    async def get_quote(self, ticker: str) -> StockQuote:
        """Fetch the latest price quote for *ticker*.

        Quotes are cached for 30 seconds.
        Raises ``NotFoundError`` when Finnhub returns a zero-price response
        (which indicates an unknown or delisted ticker).
        """
        cache_key = f"quote:{ticker}"
        cached = _quote_cache.get(cache_key)
        if cached is not None:
            logger.info("market_quote", ticker=ticker, provider=self.provider, cache_hit=True)
            return cached

        logger.info("market_quote", ticker=ticker, provider=self.provider, cache_hit=False)

        data = await self._get("/quote", {"symbol": ticker})

        # Finnhub returns all-zero fields for unknown tickers — treat as not found.
        current_price = data.get("c", 0)
        if not current_price:
            raise NotFoundError("Stock", ticker)

        # Finnhub timestamp is Unix seconds; convert to UTC datetime.
        raw_ts = data.get("t", 0)
        ts = (
            datetime.fromtimestamp(int(raw_ts), tz=timezone.utc)
            if raw_ts
            else datetime.now(tz=timezone.utc)
        )

        quote = StockQuote(
            ticker=ticker,
            price=Decimal(str(data.get("c", 0))),
            change=Decimal(str(data.get("d", 0) or 0)),
            change_percent=Decimal(str(data.get("dp", 0) or 0)),
            volume=int(data.get("v", 0) or 0),
            high=Decimal(str(data.get("h", 0))),
            low=Decimal(str(data.get("l", 0))),
            open=Decimal(str(data.get("o", 0))),
            previous_close=Decimal(str(data.get("pc", 0))),
            timestamp=ts,
        )

        _quote_cache[cache_key] = quote
        return quote

    async def get_history(self, ticker: str, time_range: str) -> StockHistory:
        """Fetch OHLCV history for *ticker* over *time_range*.

        History is cached for 300 seconds.
        Raises ``NotFoundError`` when Finnhub returns ``s='no_data'``.
        """
        cache_key = f"history:{ticker}:{time_range}"
        cached = _history_cache.get(cache_key)
        if cached is not None:
            logger.info(
                "market_history",
                ticker=ticker,
                time_range=time_range,
                provider=self.provider,
                cache_hit=True,
            )
            return cached

        logger.info(
            "market_history",
            ticker=ticker,
            time_range=time_range,
            provider=self.provider,
            cache_hit=False,
        )

        resolution = _RESOLUTION_MAP.get(time_range, "D")
        delta = _TIMEDELTA_MAP.get(time_range, timedelta(days=30))

        now = datetime.now(tz=timezone.utc)
        from_ts = int((now - delta).timestamp())
        to_ts = int(now.timestamp())

        data = await self._get(
            "/stock/candle",
            {
                "symbol": ticker,
                "resolution": resolution,
                "from": from_ts,
                "to": to_ts,
            },
        )

        status = data.get("s", "no_data")
        if status != "ok":
            raise NotFoundError("Stock history", f"{ticker}/{time_range}")

        timestamps: list[int] = data.get("t") or []  # type: ignore[assignment]
        opens: list[float] = data.get("o") or []  # type: ignore[assignment]
        highs: list[float] = data.get("h") or []  # type: ignore[assignment]
        lows: list[float] = data.get("l") or []  # type: ignore[assignment]
        closes: list[float] = data.get("c") or []  # type: ignore[assignment]
        volumes: list[int] = data.get("v") or []  # type: ignore[assignment]

        data_points = [
            PricePoint(
                timestamp=datetime.fromtimestamp(ts, tz=timezone.utc),
                open=Decimal(str(o)),
                high=Decimal(str(h)),
                low=Decimal(str(lv)),
                close=Decimal(str(c)),
                volume=int(v),
            )
            for ts, o, h, lv, c, v in zip(timestamps, opens, highs, lows, closes, volumes)
        ]

        history = StockHistory(
            ticker=ticker,
            time_range=time_range,
            interval=resolution,
            data_points=data_points,
        )

        _history_cache[cache_key] = history
        return history
