import uuid

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Watchlist(TimestampMixin, Base):
    __tablename__ = "watchlists"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    user: Mapped["User"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "User", back_populates="watchlists"
    )
    items: Mapped[list["WatchlistItem"]] = relationship(
        "WatchlistItem", back_populates="watchlist", cascade="all, delete-orphan"
    )


class WatchlistItem(TimestampMixin, Base):
    __tablename__ = "watchlist_items"

    __table_args__ = (
        UniqueConstraint("watchlist_id", "ticker", name="uq_watchlist_ticker"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    watchlist_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("watchlists.id", ondelete="CASCADE"), index=True
    )
    ticker: Mapped[str] = mapped_column(String(10), nullable=False)
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)

    watchlist: Mapped["Watchlist"] = relationship("Watchlist", back_populates="items")
