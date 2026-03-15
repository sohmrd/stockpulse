import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class PortfolioCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)


class PortfolioUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)


class HoldingCreate(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10)
    quantity: Decimal = Field(..., gt=0)
    average_cost: Decimal = Field(..., gt=0)


class HoldingResponse(BaseModel):
    id: uuid.UUID
    ticker: str
    quantity: Decimal
    average_cost: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}


class TransactionCreate(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10)
    transaction_type: str = Field(..., pattern=r"^(buy|sell)$")
    quantity: Decimal = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)
    transacted_at: datetime
    notes: str | None = Field(None, max_length=500)


class TransactionResponse(BaseModel):
    id: uuid.UUID
    ticker: str
    transaction_type: str
    quantity: Decimal
    price: Decimal
    transacted_at: datetime
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class PortfolioResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    holdings: list[HoldingResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
