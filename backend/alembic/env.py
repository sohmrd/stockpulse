"""Alembic migration environment — async-aware, reads config from pydantic-settings."""

from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# Import settings so the sync URL is always read from the environment
from app.core.config import settings

# Import all models so Alembic's autogenerate can detect changes
import app.models  # noqa: F401 — side-effect import registers all models
from app.db.base import Base

# ── Alembic config object ─────────────────────────────────────────────────────
config = context.config

# Inject the sync database URL from pydantic-settings at runtime
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL_SYNC)

# Set up Python logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# ── Offline migrations (no live DB connection required) ───────────────────────


def run_migrations_offline() -> None:
    """Run migrations without a DB connection — outputs SQL to stdout."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


# ── Online migrations (connects to DB) ────────────────────────────────────────


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations using an async engine (asyncpg / aiosqlite)."""
    # Build an async engine from the *sync* URL by swapping the driver prefix
    async_url = settings.DATABASE_URL  # already async (asyncpg / aiosqlite)
    connectable = async_engine_from_config(
        {"sqlalchemy.url": async_url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
