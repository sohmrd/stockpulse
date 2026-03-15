"""Insights endpoint tests."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_trend_requires_auth(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/v1/insights/trend",
        json={"ticker": "AAPL", "time_range": "1M"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_trend_validates_time_range(auth_client: AsyncClient) -> None:
    resp = await auth_client.post(
        "/api/v1/insights/trend",
        json={"ticker": "AAPL", "time_range": "INVALID"},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_trend_stub_returns_envelope(auth_client: AsyncClient) -> None:
    resp = await auth_client.post(
        "/api/v1/insights/trend",
        json={"ticker": "aapl", "time_range": "1M"},  # lowercase — should be uppercased
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["error"] is None
    assert body["data"]["sentiment"] == "neutral"
    # Disclaimer must be present
    assert "not financial advice" in body["data"]["disclaimer"]
