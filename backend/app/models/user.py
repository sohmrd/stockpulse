import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    # relationships (populated once other models exist)
    portfolios: Mapped[list["Portfolio"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Portfolio", back_populates="user", lazy="select"
    )
    watchlists: Mapped[list["Watchlist"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Watchlist", back_populates="user", lazy="select"
    )
    alerts: Mapped[list["Alert"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Alert", back_populates="user", lazy="select"
    )
