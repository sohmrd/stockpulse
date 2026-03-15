"""Alert service — evaluation and notification triggering for price-threshold alerts."""

from __future__ import annotations

import uuid

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.alert import AlertCreate, AlertResponse, AlertUpdate

logger = structlog.get_logger()


class AlertService:
    """Business logic for alert CRUD and evaluation.

    TODO (Sprint 5): implement evaluation loop via BackgroundTasks or Celery.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_alerts(self, user_id: uuid.UUID) -> list[AlertResponse]:
        logger.info("alert_list", user_id=str(user_id))
        return []

    async def create_alert(
        self, user_id: uuid.UUID, data: AlertCreate
    ) -> AlertResponse:
        raise NotImplementedError("AlertService.create_alert is not yet implemented.")

    async def update_alert(
        self, alert_id: uuid.UUID, user_id: uuid.UUID, data: AlertUpdate
    ) -> AlertResponse:
        raise NotImplementedError("AlertService.update_alert is not yet implemented.")

    async def delete_alert(self, alert_id: uuid.UUID, user_id: uuid.UUID) -> None:
        raise NotImplementedError("AlertService.delete_alert is not yet implemented.")
