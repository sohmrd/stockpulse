"""AI insights endpoints — trend analysis and portfolio suggestions (Claude-powered)."""

from __future__ import annotations

from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api.deps import CurrentUser, get_claude_service
from app.core.config import settings
from app.schemas.common import APIResponse
from app.schemas.insights import SuggestionRequest, SuggestionResponse, TrendInsight, TrendRequest
from app.services.claude_service import ClaudeService

router = APIRouter(prefix="/insights", tags=["insights"])


@router.post("/trend", response_model=APIResponse[TrendInsight])
async def get_trend(
    body: TrendRequest,
    _user: CurrentUser,
    claude: ClaudeService = Depends(get_claude_service),
) -> APIResponse[TrendInsight]:
    """Return a structured AI trend analysis for a ticker."""
    insight = await claude.get_trend_analysis(
        ticker=body.ticker,
        time_range=body.time_range,
        news_snippets=None,
    )
    return APIResponse(
        data=insight,
        meta={"model": settings.CLAUDE_MODEL_PRIMARY},
    )


@router.post("/trend/stream")
async def stream_trend(
    body: TrendRequest,
    _user: CurrentUser,
    claude: ClaudeService = Depends(get_claude_service),
) -> StreamingResponse:
    """Stream AI trend analysis as server-sent events."""

    async def _event_stream() -> AsyncGenerator[str, None]:
        async for chunk in claude.stream_trend_analysis(body.ticker, body.time_range):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(_event_stream(), media_type="text/event-stream")


@router.post("/suggest", response_model=APIResponse[SuggestionResponse])
async def get_suggestions(
    body: SuggestionRequest,
    _user: CurrentUser,
    claude: ClaudeService = Depends(get_claude_service),
) -> APIResponse[SuggestionResponse]:
    """Return AI-generated portfolio rebalancing suggestions."""
    suggestion = await claude.get_suggestion(
        portfolio_summary=body.portfolio_id,
        risk_profile=body.risk_profile,
    )
    return APIResponse(
        data=suggestion,
        meta={"model": settings.CLAUDE_MODEL_PRIMARY},
    )
