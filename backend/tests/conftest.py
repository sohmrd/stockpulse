"""Shared pytest fixtures for the StockPulse backend test suite."""

from __future__ import annotations

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base
from app.db.session import get_db
from app.main import create_app

# ── In-memory SQLite for tests ────────────────────────────────────────────────
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_stockpulse.db"


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh test database for each test, then tear it down."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Unauthenticated async test client with DB override."""
    app = create_app()
    app.dependency_overrides[get_db] = lambda: db_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as ac:
        yield ac


@pytest.fixture
async def auth_client(client: AsyncClient) -> AsyncGenerator[AsyncClient, None]:
    """Authenticated test client — registers + logs in a test user."""
    reg_resp = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "testuser@example.com",
            "password": "Str0ngP@ss!",
            "display_name": "Test User",
        },
    )
    assert reg_resp.status_code == 201, reg_resp.text

    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "testuser@example.com", "password": "Str0ngP@ss!"},
    )
    assert login_resp.status_code == 200, login_resp.text

    access_token: str = login_resp.json()["data"]["access_token"]
    client.headers["Authorization"] = f"Bearer {access_token}"
    yield client
    # Clean up auth header so the fixture can be re-used safely
    client.headers.pop("Authorization", None)
