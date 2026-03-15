from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class StockSearchResult(BaseModel):
    ticker: str
    name: str
    exchange: str
    asset_type: str = "Equity"


class StockQuote(BaseModel):
    ticker: str
    price: Decimal
    change: Decimal
    change_percent: Decimal
    volume: int
    market_cap: Decimal | None = None
    high: Decimal
    low: Decimal
    open: Decimal
    previous_close: Decimal
    timestamp: datetime


class PricePoint(BaseModel):
    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


class StockHistory(BaseModel):
    ticker: str
    time_range: str = Field(..., pattern=r"^(1D|1W|1M|3M|6M|1Y|5Y)$")
    interval: str
    data_points: list[PricePoint]
