from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ── Password helpers ──────────────────────────────────────────────────────────


def hash_password(plain: str) -> str:
    """Return a bcrypt hash of *plain*."""
    return _pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Return True when *plain* matches *hashed*."""
    return _pwd_context.verify(plain, hashed)


# ── JWT helpers ───────────────────────────────────────────────────────────────


def create_access_token(subject: str) -> str:
    """Create a short-lived JWT access token for *subject* (user UUID string)."""
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=settings.JWT_EXPIRATION_MINUTES
    )
    payload: dict[str, Any] = {
        "sub": subject,
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(subject: str) -> str:
    """Create a long-lived JWT refresh token for *subject* (user UUID string)."""
    expire = datetime.now(tz=timezone.utc) + timedelta(
        days=settings.JWT_REFRESH_EXPIRATION_DAYS
    )
    payload: dict[str, Any] = {
        "sub": subject,
        "exp": expire,
        "type": "refresh",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_token(token: str, expected_type: str = "access") -> str:
    """Decode and validate *token*.

    Returns the ``sub`` claim (user UUID string) on success.
    Raises ``jwt.PyJWTError`` on any failure (expired, wrong type, bad signature).
    """
    payload: dict[str, Any] = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
    token_type: str = payload.get("type", "")
    if token_type != expected_type:
        raise jwt.InvalidTokenError(
            f"Expected token type '{expected_type}', got '{token_type}'"
        )
    subject: str = payload["sub"]
    return subject
