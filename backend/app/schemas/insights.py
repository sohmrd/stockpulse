from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class TrendRequest(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=5, examples=["AAPL"])
    time_range: str = Field(..., pattern=r"^(1D|1W|1M|3M|6M|1Y|5Y)$")
    include_news: bool = False

    @field_validator("ticker")
    @classmethod
    def uppercase_ticker(cls, v: str) -> str:
        return v.upper().strip()


class TrendInsight(BaseModel):
    summary: str
    sentiment: str = Field(..., pattern=r"^(bullish|bearish|neutral)$")
    confidence: float = Field(..., ge=0.0, le=1.0)
    key_points: list[str]
    disclaimer: str = (
        "This is AI-generated analysis for informational purposes only. "
        "It is not financial advice. Always consult a qualified financial advisor "
        "before making investment decisions."
    )
    generated_at: datetime
    tokens_used: int


class TrendResponse(BaseModel):
    data: TrendInsight | None = None
    error: str | None = None
    meta: dict[str, object] | None = None


class SuggestionRequest(BaseModel):
    portfolio_id: str
    risk_profile: str | None = Field(
        None, pattern=r"^(conservative|moderate|aggressive)$"
    )


class SuggestionResponse(BaseModel):
    suggestions: list[str]
    reasoning: str
    disclaimer: str = (
        "This is AI-generated analysis for informational purposes only. "
        "It is not financial advice. Always consult a qualified financial advisor "
        "before making investment decisions."
    )
    generated_at: datetime
    tokens_used: int
