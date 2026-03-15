"""Stock endpoint tests (stub-level — real data fetching tested in Sprint 2)."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_search_requires_auth(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/stocks/search", params={"q": "AAPL"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_search_validates_empty_query(auth_client: AsyncClient) -> None:
    resp = await auth_client.get("/api/v1/stocks/search", params={"q": ""})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_search_returns_envelope(auth_client: AsyncClient) -> None:
    # MarketService is a stub; it returns [] without raising.
    resp = await auth_client.get("/api/v1/stocks/search", params={"q": "AAPL"})
    assert resp.status_code == 200
    body = resp.json()
    assert "data" in body
    assert "error" in body
