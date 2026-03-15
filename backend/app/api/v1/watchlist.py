"""Watchlist endpoints — CRUD for watchlists and their items."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.deps import CurrentUser, DBSession
from app.schemas.common import APIResponse
from app.schemas.watchlist import WatchlistCreate, WatchlistItemCreate, WatchlistResponse

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.get("", response_model=APIResponse[list[WatchlistResponse]])
async def list_watchlists(
    _user: CurrentUser,
    _db: DBSession,
) -> APIResponse[list[WatchlistResponse]]:
    """List all watchlists for the authenticated user.

    TODO (Sprint 2): implement via WatchlistService.
    """
    return APIResponse(data=[], meta={})


@router.post("", response_model=APIResponse[WatchlistResponse], status_code=201)
async def create_watchlist(
    _body: WatchlistCreate,
    _user: CurrentUser,
    _db: DBSession,
) -> APIResponse[WatchlistResponse]:
    """Create a new watchlist.

    TODO (Sprint 2): implement via WatchlistService.
    """
    return APIResponse(data=None, meta={})


@router.post("/{watchlist_id}/items", response_model=APIResponse[WatchlistResponse])
async def add_item(
    watchlist_id: str,
    _body: WatchlistItemCreate,
    _user: CurrentUser,
    _db: DBSession,
) -> APIResponse[WatchlistResponse]:
    """Add a ticker to a watchlist.

    TODO (Sprint 2): implement via WatchlistService.
    """
    return APIResponse(data=None, meta={"watchlist_id": watchlist_id})


@router.delete("/{watchlist_id}/items/{ticker}", response_model=APIResponse[None])
async def remove_item(
    watchlist_id: str,
    ticker: str,
    _user: CurrentUser,
    _db: DBSession,
) -> APIResponse[None]:
    """Remove a ticker from a watchlist.

    TODO (Sprint 2): implement via WatchlistService.
    """
    return APIResponse(data=None, meta={"watchlist_id": watchlist_id, "ticker": ticker})
