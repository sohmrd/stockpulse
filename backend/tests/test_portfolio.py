"""Portfolio endpoint tests (stub-level — full service logic tested in Sprint 3)."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_portfolios_requires_auth(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/portfolio")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_list_portfolios_returns_empty_for_new_user(auth_client: AsyncClient) -> None:
    resp = await auth_client.get("/api/v1/portfolio")
    assert resp.status_code == 200
    body = resp.json()
    assert body["data"] == []
    assert body["error"] is None
