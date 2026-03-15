# Backend Agent — Sprint 2 Learnings

## Permissions issue
- Subagent subprocess sessions block Write and Edit tools
- Agents must be resumed with explicit permission grants from TPM
- Always state clearly when permissions are needed so TPM can act quickly

## API client vs backend contract mismatch (caught in Sprint 2)
- Frontend `watchlistApi.removeItem(watchlistId, itemId)` sends DELETE to `.../items/{itemId}`
  but backend stub endpoint was `.../items/{ticker}`
- Backend watchlist.py must use `{item_id}` path param (UUID), not `{ticker}`
- `watchlistApi.addItem` returns `WatchlistItem` per the frontend client, but backend was returning full `Watchlist`
  - Need to align: either backend returns WatchlistItem or frontend client is updated

## Exception classes in exceptions.py (verified)
- `AppError` — base, takes message + status_code
- `NotFoundError`, `ConflictError`, `UnauthorizedError` already exist
- No standalone `ValidationError` — use `AppError(msg, status_code=422)` for limit exceeded cases
- `RateLimitError` (429), `ExternalServiceError` (502) needed for market data service

## MarketService design (Sprint 2)
- Module-level `TTLCache` singletons (not per-instance) so cache persists across request-scoped instances
- `httpx.AsyncClient` created in `__init__`, closed in `async close()`
- `get_market_service()` in deps.py should be an async generator that yields and calls `await service.close()`
- Finnhub candle endpoint returns parallel arrays `{c, h, l, o, v, t, s}` — zip them to build OHLCVDataPoint list
- Finnhub `s="no_data"` means raise NotFoundError

## DB patterns
- Always use `selectinload` for eager loading relationships (avoids N+1)
- After `db.flush()`, call `db.refresh(obj, ["relationship_name"])` to populate relationships for response
- Filter by both resource ID and user_id in one WHERE clause for ownership validation (returns 404 not 403)
- `uuid.UUID(str_id)` cast required when comparing JWT string user_id against UUID column

## pyproject.toml additions needed for Sprint 2
- `cachetools>=2.1.0` (market service TTLCache)
- `types-cachetools>=2.1.0` (dev dependency for mypy)
- `structlog` (already present from Sprint 1)
- `tenacity` (retry logic)
