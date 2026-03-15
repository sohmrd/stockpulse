"""FastAPI shared dependencies — DB session, current user, service factories."""

from __future__ import annotations

from typing import Annotated

import jwt
import structlog
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedError
from app.core.security import verify_token
from app.db.session import get_db
from app.models.user import User
from app.services.alert_service import AlertService
from app.services.claude_service import ClaudeService
from app.services.market_service import MarketService
from app.services.portfolio_service import PortfolioService

logger = structlog.get_logger()

_bearer_scheme = HTTPBearer(auto_error=False)

# ── Type aliases (use in route signatures for brevity) ─────────────────────────

DBSession = Annotated[AsyncSession, Depends(get_db)]


# ── Auth dependency ────────────────────────────────────────────────────────────


async def get_current_user(
    db: DBSession,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> User:
    """Decode the Bearer JWT and return the corresponding User.

    Raises ``UnauthorizedError`` (→ HTTP 401) on any failure.
    """
    if credentials is None:
        raise UnauthorizedError("Not authenticated")

    try:
        user_id = verify_token(credentials.credentials, expected_type="access")
    except jwt.PyJWTError as exc:
        logger.warning("jwt_validation_failed", error=str(exc))
        raise UnauthorizedError("Invalid or expired token") from exc

    stmt = select(User).where(User.id == user_id)  # type: ignore[arg-type]
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise UnauthorizedError("User not found or inactive")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


# ── Service factories ──────────────────────────────────────────────────────────


def get_claude_service() -> ClaudeService:
    return ClaudeService()


def get_market_service() -> MarketService:
    return MarketService()


def get_portfolio_service(db: DBSession) -> PortfolioService:
    return PortfolioService(db=db)


def get_alert_service(db: DBSession) -> AlertService:
    return AlertService(db=db)
