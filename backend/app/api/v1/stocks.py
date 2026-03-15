"""Stock endpoints — search, quote, historical data."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.api.deps import CurrentUser, get_market_service
from app.schemas.common import APIResponse
from app.schemas.stock import StockHistory, StockQuote, StockSearchResult
from app.services.market_service import MarketService

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("/search", response_model=APIResponse[list[StockSearchResult]])
async def search_stocks(
    _user: CurrentUser,
    q: str = Query(..., min_length=1, max_length=50),
    market: MarketService = Depends(get_market_service),
) -> APIResponse[list[StockSearchResult]]:
    """Search for stocks by keyword or ticker symbol."""
    results = await market.search(q)
    return APIResponse(data=results, meta={"query": q})


@router.get("/{ticker}/quote", response_model=APIResponse[StockQuote])
async def get_quote(
    ticker: str,
    _user: CurrentUser,
    market: MarketService = Depends(get_market_service),
) -> APIResponse[StockQuote]:
    """Fetch the latest price quote for a ticker."""
    quote = await market.get_quote(ticker.upper())
    return APIResponse(data=quote, meta={"source": "market_service"})


@router.get("/{ticker}/history", response_model=APIResponse[StockHistory])
async def get_history(
    ticker: str,
    _user: CurrentUser,
    time_range: str = Query(..., pattern=r"^(1D|1W|1M|3M|6M|1Y|5Y)$"),
    market: MarketService = Depends(get_market_service),
) -> APIResponse[StockHistory]:
    """Fetch OHLCV price history for a ticker."""
    history = await market.get_history(ticker.upper(), time_range)
    return APIResponse(data=history, meta={"ticker": ticker, "time_range": time_range})
