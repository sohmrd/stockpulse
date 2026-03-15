"""Portfolio service — P&L calculation, holding management, transaction processing."""

from __future__ import annotations

import uuid

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.portfolio import (
    HoldingCreate,
    PortfolioCreate,
    PortfolioResponse,
    TransactionCreate,
    TransactionResponse,
)

logger = structlog.get_logger()


class PortfolioService:
    """Business logic for portfolio operations.

    TODO (Sprint 3): implement full CRUD, P&L, and allocation logic.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_portfolios(self, user_id: uuid.UUID) -> list[PortfolioResponse]:
        logger.info("portfolio_list", user_id=str(user_id))
        return []

    async def create_portfolio(
        self, user_id: uuid.UUID, data: PortfolioCreate
    ) -> PortfolioResponse:
        logger.info("portfolio_create", user_id=str(user_id), name=data.name)
        raise NotImplementedError("PortfolioService.create_portfolio is not yet implemented.")

    async def add_holding(
        self, portfolio_id: uuid.UUID, user_id: uuid.UUID, data: HoldingCreate
    ) -> PortfolioResponse:
        raise NotImplementedError("PortfolioService.add_holding is not yet implemented.")

    async def add_transaction(
        self, portfolio_id: uuid.UUID, user_id: uuid.UUID, data: TransactionCreate
    ) -> TransactionResponse:
        raise NotImplementedError("PortfolioService.add_transaction is not yet implemented.")
