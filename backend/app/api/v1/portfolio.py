"""Portfolio endpoints — CRUD for portfolios, holdings, and transactions."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser, DBSession, get_portfolio_service
from app.schemas.common import APIResponse
from app.schemas.portfolio import (
    HoldingCreate,
    PortfolioCreate,
    PortfolioResponse,
    TransactionCreate,
    TransactionResponse,
)
from app.services.portfolio_service import PortfolioService

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("", response_model=APIResponse[list[PortfolioResponse]])
async def list_portfolios(
    user: CurrentUser,
    svc: PortfolioService = Depends(get_portfolio_service),
) -> APIResponse[list[PortfolioResponse]]:
    """List all portfolios for the authenticated user."""
    portfolios = await svc.list_portfolios(user.id)
    return APIResponse(data=portfolios)


@router.post("", response_model=APIResponse[PortfolioResponse], status_code=201)
async def create_portfolio(
    body: PortfolioCreate,
    user: CurrentUser,
    svc: PortfolioService = Depends(get_portfolio_service),
) -> APIResponse[PortfolioResponse]:
    """Create a new portfolio."""
    portfolio = await svc.create_portfolio(user.id, body)
    return APIResponse(data=portfolio)


@router.post("/{portfolio_id}/holdings", response_model=APIResponse[PortfolioResponse])
async def add_holding(
    portfolio_id: uuid.UUID,
    body: HoldingCreate,
    user: CurrentUser,
    svc: PortfolioService = Depends(get_portfolio_service),
) -> APIResponse[PortfolioResponse]:
    """Add or update a holding in a portfolio."""
    portfolio = await svc.add_holding(portfolio_id, user.id, body)
    return APIResponse(data=portfolio)


@router.post(
    "/{portfolio_id}/transactions",
    response_model=APIResponse[TransactionResponse],
    status_code=201,
)
async def add_transaction(
    portfolio_id: uuid.UUID,
    body: TransactionCreate,
    user: CurrentUser,
    svc: PortfolioService = Depends(get_portfolio_service),
) -> APIResponse[TransactionResponse]:
    """Record a buy or sell transaction against a portfolio."""
    transaction = await svc.add_transaction(portfolio_id, user.id, body)
    return APIResponse(data=transaction)
