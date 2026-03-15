import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class AlertCreate(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10)
    condition: str = Field(..., pattern=r"^(above|below)$")
    threshold: Decimal = Field(..., gt=0)
    notification_message: str | None = Field(None, max_length=500)


class AlertUpdate(BaseModel):
    threshold: Decimal | None = Field(None, gt=0)
    condition: str | None = Field(None, pattern=r"^(above|below)$")
    is_active: bool | None = None
    notification_message: str | None = Field(None, max_length=500)


class AlertResponse(BaseModel):
    id: uuid.UUID
    ticker: str
    condition: str
    threshold: Decimal
    is_active: bool
    is_triggered: bool
    notification_message: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
