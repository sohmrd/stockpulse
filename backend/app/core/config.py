from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ───────────────────────────────────────────────────────────────────
    APP_ENV: str = "development"
    SECRET_KEY: str = "change-me"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # ── Database ──────────────────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite+aiosqlite:///./stockpulse_dev.db"
    DATABASE_URL_SYNC: str = "sqlite:///./stockpulse_dev.db"

    # ── Auth ──────────────────────────────────────────────────────────────────
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60
    JWT_REFRESH_EXPIRATION_DAYS: int = 7
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    # ── Market Data ───────────────────────────────────────────────────────────
    MARKET_DATA_API_KEY: str = ""
    MARKET_DATA_PROVIDER: str = "alpha_vantage"

    # ── Claude API ────────────────────────────────────────────────────────────
    ANTHROPIC_API_KEY: str = ""
    CLAUDE_MODEL_PRIMARY: str = "claude-sonnet-4-20250514"
    CLAUDE_MODEL_LIGHTWEIGHT: str = "claude-haiku-4-5-20251001"
    CLAUDE_MAX_TOKENS_TREND: int = 2048
    CLAUDE_MAX_TOKENS_SUGGESTION: int = 4096
    CLAUDE_ENABLED: bool = True

    # ── Cache ─────────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── Monitoring ────────────────────────────────────────────────────────────
    SENTRY_DSN: str = ""

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        """Accept a JSON array string or a plain comma-separated string."""
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            v = v.strip()
            if v.startswith("["):
                import json

                return json.loads(v)  # type: ignore[no-any-return]
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v


settings = Settings()
