import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Portfolio(TimestampMixin, Base):
    __tablename__ = "portfolios"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    user: Mapped["User"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "User", back_populates="portfolios"
    )
    holdings: Mapped[list["Holding"]] = relationship(
        "Holding", back_populates="portfolio", cascade="all, delete-orphan"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="portfolio", cascade="all, delete-orphan"
    )


class Holding(TimestampMixin, Base):
    __tablename__ = "holdings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"), index=True
    )
    ticker: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    average_cost: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)

    portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="holdings")


class Transaction(TimestampMixin, Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"), index=True
    )
    ticker: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    # "buy" | "sell"
    transaction_type: Mapped[str] = mapped_column(String(4), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    transacted_at: Mapped[datetime] = mapped_column(nullable=False)
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)

    portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="transactions")
