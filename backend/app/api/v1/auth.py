"""Authentication endpoints — register, login, token refresh."""

from __future__ import annotations

import uuid

import jwt
import structlog
from fastapi import APIRouter
from sqlalchemy import select

from app.api.deps import CurrentUser, DBSession
from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    verify_token,
)
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.user import RefreshRequest, TokenPair, UserCreate, UserLogin, UserResponse

logger = structlog.get_logger()

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=APIResponse[TokenPair], status_code=201)
async def register(body: UserCreate, db: DBSession) -> APIResponse[TokenPair]:
    """Create a new user account and return a token pair."""
    stmt = select(User).where(User.email == body.email)
    existing = (await db.execute(stmt)).scalar_one_or_none()
    if existing is not None:
        raise ConflictError("User", body.email)

    user = User(
        email=body.email,
        hashed_password=hash_password(body.password),
        display_name=body.display_name,
    )
    db.add(user)
    await db.flush()  # populate user.id before token creation

    logger.info("user_registered", user_id=str(user.id), email=body.email)

    tokens = TokenPair(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )
    return APIResponse(data=tokens)


@router.post("/login", response_model=APIResponse[TokenPair])
async def login(body: UserLogin, db: DBSession) -> APIResponse[TokenPair]:
    """Validate credentials and return a token pair."""
    stmt = select(User).where(User.email == body.email)
    user = (await db.execute(stmt)).scalar_one_or_none()

    if user is None or not verify_password(body.password, user.hashed_password):
        logger.warning("login_failed", email=body.email)
        raise UnauthorizedError("Invalid email or password")

    if not user.is_active:
        raise UnauthorizedError("Account is disabled")

    logger.info("login_success", user_id=str(user.id))
    tokens = TokenPair(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )
    return APIResponse(data=tokens)


@router.post("/refresh", response_model=APIResponse[TokenPair])
async def refresh(body: RefreshRequest, db: DBSession) -> APIResponse[TokenPair]:
    """Exchange a valid refresh token for a new token pair."""
    try:
        user_id = verify_token(body.refresh_token, expected_type="refresh")
    except jwt.PyJWTError as exc:
        raise UnauthorizedError("Invalid or expired refresh token") from exc

    stmt = select(User).where(User.id == uuid.UUID(user_id))
    user = (await db.execute(stmt)).scalar_one_or_none()
    if user is None or not user.is_active:
        raise UnauthorizedError("User not found or inactive")

    logger.info("token_refreshed", user_id=str(user.id))
    tokens = TokenPair(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )
    return APIResponse(data=tokens)


@router.get("/me", response_model=APIResponse[UserResponse])
async def me(user: CurrentUser) -> APIResponse[UserResponse]:
    """Return the profile of the currently authenticated user."""
    return APIResponse(data=UserResponse.model_validate(user))
