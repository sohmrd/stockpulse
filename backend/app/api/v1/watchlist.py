"""Watchlist endpoints — CRUD for watchlists and their items."""

from __future__ import annotations

import uuid

import structlog
from fastapi import APIRouter
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.api.deps import CurrentUser, DBSession
from app.core.exceptions import AppError, ConflictError, NotFoundError
from app.models.watchlist import Watchlist, WatchlistItem
from app.schemas.common import APIResponse
from app.schemas.watchlist import WatchlistCreate, WatchlistItemCreate, WatchlistItemResponse, WatchlistResponse

logger = structlog.get_logger()

router = APIRouter(prefix="/watchlist", tags=["watchlist"])

_MAX_WATCHLISTS_PER_USER = 10
_MAX_ITEMS_PER_WATCHLIST = 50


# ── Helpers ────────────────────────────────────────────────────────────────────


async def _get_watchlist_for_user(
    db: DBSession,
    watchlist_id: str,
    user_id: uuid.UUID,
    *,
    load_items: bool = True,
) -> Watchlist:
    """Fetch watchlist by ID, validating ownership. Raises NotFoundError (404) on miss."""
    stmt = select(Watchlist).where(
        Watchlist.id == uuid.UUID(watchlist_id),
        Watchlist.user_id == user_id,
    )
    if load_items:
        stmt = stmt.options(selectinload(Watchlist.items))

    watchlist = (await db.execute(stmt)).scalar_one_or_none()
    if watchlist is None:
        raise NotFoundError("Watchlist", watchlist_id)
    return watchlist


# ── Endpoints ──────────────────────────────────────────────────────────────────


@router.get("", response_model=APIResponse[list[WatchlistResponse]])
async def list_watchlists(
    user: CurrentUser,
    db: DBSession,
) -> APIResponse[list[WatchlistResponse]]:
    """List all watchlists for the authenticated user, including items."""
    stmt = (
        select(Watchlist)
        .options(selectinload(Watchlist.items))
        .where(Watchlist.user_id == user.id)
        .order_by(Watchlist.created_at)
    )
    watchlists = list((await db.execute(stmt)).scalars().all())
    logger.info("watchlists_listed", user_id=str(user.id), count=len(watchlists))
    return APIResponse(
        data=[WatchlistResponse.model_validate(w) for w in watchlists],
        meta={"count": len(watchlists)},
    )


@router.post("", response_model=APIResponse[WatchlistResponse], status_code=201)
async def create_watchlist(
    body: WatchlistCreate,
    user: CurrentUser,
    db: DBSession,
) -> APIResponse[WatchlistResponse]:
    """Create a new watchlist (max 10 per user)."""
    count_stmt = select(func.count()).select_from(Watchlist).where(Watchlist.user_id == user.id)
    count = (await db.execute(count_stmt)).scalar_one()
    if count >= _MAX_WATCHLISTS_PER_USER:
        raise AppError(
            f"Watchlist limit reached ({_MAX_WATCHLISTS_PER_USER} max).",
            status_code=422,
        )

    watchlist = Watchlist(user_id=user.id, name=body.name)
    db.add(watchlist)
    await db.flush()
    await db.refresh(watchlist, ["items"])

    logger.info("watchlist_created", user_id=str(user.id), watchlist_id=str(watchlist.id))
    return APIResponse(data=WatchlistResponse.model_validate(watchlist))


@router.post("/{watchlist_id}/items", response_model=APIResponse[WatchlistItemResponse])
async def add_item(
    watchlist_id: str,
    body: WatchlistItemCreate,
    user: CurrentUser,
    db: DBSession,
) -> APIResponse[WatchlistItemResponse]:
    """Add a ticker to a watchlist (max 50 items)."""
    watchlist = await _get_watchlist_for_user(db, watchlist_id, user.id)

    ticker = body.ticker.upper().strip()

    if len(watchlist.items) >= _MAX_ITEMS_PER_WATCHLIST:
        raise AppError(
            f"Watchlist item limit reached ({_MAX_ITEMS_PER_WATCHLIST} max).",
            status_code=422,
        )

    if any(i.ticker == ticker for i in watchlist.items):
        raise ConflictError("WatchlistItem", ticker)

    item = WatchlistItem(watchlist_id=watchlist.id, ticker=ticker, notes=body.notes)
    db.add(item)
    await db.flush()
    await db.refresh(item)

    logger.info("watchlist_item_added", user_id=str(user.id), watchlist_id=watchlist_id, ticker=ticker)
    return APIResponse(data=WatchlistItemResponse.model_validate(item))


@router.delete("/{watchlist_id}/items/{item_id}", response_model=APIResponse[WatchlistResponse])
async def remove_item(
    watchlist_id: str,
    item_id: str,
    user: CurrentUser,
    db: DBSession,
) -> APIResponse[WatchlistResponse]:
    """Remove an item from a watchlist by item ID."""
    watchlist = await _get_watchlist_for_user(db, watchlist_id, user.id)

    item = next((i for i in watchlist.items if str(i.id) == item_id), None)
    if item is None:
        raise NotFoundError("WatchlistItem", item_id)

    await db.delete(item)
    await db.flush()
    await db.refresh(watchlist, ["items"])

    logger.info("watchlist_item_removed", user_id=str(user.id), watchlist_id=watchlist_id, item_id=item_id)
    return APIResponse(data=WatchlistResponse.model_validate(watchlist))


@router.delete("/{watchlist_id}", response_model=APIResponse[None], status_code=204)
async def delete_watchlist(
    watchlist_id: str,
    user: CurrentUser,
    db: DBSession,
) -> APIResponse[None]:
    """Delete a watchlist and all its items."""
    watchlist = await _get_watchlist_for_user(db, watchlist_id, user.id, load_items=False)
    await db.delete(watchlist)
    await db.flush()

    logger.info("watchlist_deleted", user_id=str(user.id), watchlist_id=watchlist_id)
    return APIResponse(data=None)
