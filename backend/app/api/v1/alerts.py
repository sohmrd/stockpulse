"""Alert endpoints — CRUD for price-threshold alerts."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser, get_alert_service
from app.schemas.alert import AlertCreate, AlertResponse, AlertUpdate
from app.schemas.common import APIResponse
from app.services.alert_service import AlertService

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=APIResponse[list[AlertResponse]])
async def list_alerts(
    user: CurrentUser,
    svc: AlertService = Depends(get_alert_service),
) -> APIResponse[list[AlertResponse]]:
    """List all alerts for the authenticated user."""
    alerts = await svc.list_alerts(user.id)
    return APIResponse(data=alerts)


@router.post("", response_model=APIResponse[AlertResponse], status_code=201)
async def create_alert(
    body: AlertCreate,
    user: CurrentUser,
    svc: AlertService = Depends(get_alert_service),
) -> APIResponse[AlertResponse]:
    """Create a new price-threshold alert."""
    alert = await svc.create_alert(user.id, body)
    return APIResponse(data=alert)


@router.patch("/{alert_id}", response_model=APIResponse[AlertResponse])
async def update_alert(
    alert_id: uuid.UUID,
    body: AlertUpdate,
    user: CurrentUser,
    svc: AlertService = Depends(get_alert_service),
) -> APIResponse[AlertResponse]:
    """Update an existing alert."""
    alert = await svc.update_alert(alert_id, user.id, body)
    return APIResponse(data=alert)


@router.delete("/{alert_id}", response_model=APIResponse[None])
async def delete_alert(
    alert_id: uuid.UUID,
    user: CurrentUser,
    svc: AlertService = Depends(get_alert_service),
) -> APIResponse[None]:
    """Delete an alert."""
    await svc.delete_alert(alert_id, user.id)
    return APIResponse(data=None, meta={"deleted": str(alert_id)})
