import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class WatchlistCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class WatchlistUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)


class WatchlistItemCreate(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10)
    notes: str | None = Field(None, max_length=500)


class WatchlistItemResponse(BaseModel):
    id: uuid.UUID
    ticker: str
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class WatchlistResponse(BaseModel):
    id: uuid.UUID
    name: str
    items: list[WatchlistItemResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
