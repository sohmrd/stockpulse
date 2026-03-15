"""Claude API service — wraps anthropic SDK calls for trend and suggestion features."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from datetime import datetime, timezone

import structlog

from app.core.config import settings
from app.core.exceptions import AIDisabledError
from app.schemas.insights import SuggestionResponse, TrendInsight

logger = structlog.get_logger()


class ClaudeService:
    """Handles all Claude API interactions.

    Instantiated once per request via FastAPI dependency injection.
    """

    def _assert_enabled(self) -> None:
        if not settings.CLAUDE_ENABLED:
            raise AIDisabledError()

    async def get_trend_analysis(
        self,
        ticker: str,
        time_range: str,
        news_snippets: list[str] | None = None,
    ) -> TrendInsight:
        """Return a structured trend insight for *ticker* over *time_range*.

        TODO (Sprint 4): implement full prompt loading, API call, and response parsing.
        """
        self._assert_enabled()

        logger.info("claude_trend_request", ticker=ticker, time_range=time_range)

        # Stub response — replace with real API call in Sprint 4
        return TrendInsight(
            summary=f"Trend analysis for {ticker} over {time_range} is not yet implemented.",
            sentiment="neutral",
            confidence=0.0,
            key_points=["Stub response — AI integration pending."],
            generated_at=datetime.now(tz=timezone.utc),
            tokens_used=0,
        )

    async def stream_trend_analysis(
        self,
        ticker: str,
        time_range: str,
    ) -> AsyncGenerator[str, None]:
        """Yield streamed text chunks for the trend analysis SSE endpoint.

        TODO (Sprint 4): implement streaming via anthropic client.messages.stream().
        """
        self._assert_enabled()

        logger.info("claude_trend_stream_request", ticker=ticker, time_range=time_range)

        # Stub: yield a single chunk then stop
        yield f"Trend analysis for {ticker} over {time_range} is not yet implemented."

    async def get_suggestion(
        self,
        portfolio_summary: str,
        risk_profile: str | None = None,
    ) -> SuggestionResponse:
        """Return AI-generated portfolio suggestions.

        TODO (Sprint 4): implement full prompt loading, API call, and response parsing.
        """
        self._assert_enabled()

        logger.info("claude_suggestion_request", risk_profile=risk_profile)

        return SuggestionResponse(
            suggestions=["Stub response — AI integration pending."],
            reasoning="AI integration is not yet implemented.",
            generated_at=datetime.now(tz=timezone.utc),
            tokens_used=0,
        )
