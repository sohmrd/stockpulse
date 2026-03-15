import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Alert(TimestampMixin, Base):
    """Price-threshold alert for a ticker owned by a user."""

    __tablename__ = "alerts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    ticker: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    # "above" | "below"
    condition: Mapped[str] = mapped_column(String(5), nullable=False)
    threshold: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_triggered: Mapped[bool] = mapped_column(default=False)
    notification_message: Mapped[str | None] = mapped_column(String(500), nullable=True)

    user: Mapped["User"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "User", back_populates="alerts"
    )
