"""Auth endpoint tests."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_creates_user(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "alice@example.com",
            "password": "P@ssword123",
            "display_name": "Alice",
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["error"] is None
    assert body["data"]["access_token"]
    assert body["data"]["refresh_token"]


@pytest.mark.asyncio
async def test_register_duplicate_email_returns_409(client: AsyncClient) -> None:
    payload = {
        "email": "bob@example.com",
        "password": "P@ssword123",
        "display_name": "Bob",
    }
    await client.post("/api/v1/auth/register", json=payload)
    resp = await client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login_returns_tokens(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "carol@example.com",
            "password": "P@ssword123",
            "display_name": "Carol",
        },
    )
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "carol@example.com", "password": "P@ssword123"},
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["access_token"]


@pytest.mark.asyncio
async def test_login_bad_password_returns_401(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "dave@example.com",
            "password": "P@ssword123",
            "display_name": "Dave",
        },
    )
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "dave@example.com", "password": "WrongPassword!"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_refresh_returns_new_tokens(client: AsyncClient) -> None:
    reg = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "eve@example.com",
            "password": "P@ssword123",
            "display_name": "Eve",
        },
    )
    refresh_token = reg.json()["data"]["refresh_token"]
    resp = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["access_token"]


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient) -> None:
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
