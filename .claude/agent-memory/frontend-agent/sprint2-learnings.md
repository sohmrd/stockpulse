# Frontend Agent — Sprint 2 Learnings

## API Client facts (verified by reading api-client.ts)
- `stocksApi.search(query)` → `StockSearchResult[]`
- `stocksApi.getQuote(ticker)` → `StockQuote`
- `stocksApi.getHistorical(ticker, timeRange)` → `StockHistoricalData` with `data_points: OHLCVDataPoint[]`
  - NOTE: method is `getHistorical`, NOT `getHistory`
- `watchlistApi.list()` → `Watchlist[]`
- `watchlistApi.addItem(watchlistId, ticker)` → `WatchlistItem` (NOT Watchlist)
- `watchlistApi.removeItem(watchlistId, itemId)` → takes the WatchlistItem `id`, NOT the ticker string

## Type facts (verified by reading types/index.ts)
- `StockSearchResult`: `{ ticker, company_name, exchange, asset_type }`
- `OHLCVDataPoint`: `{ timestamp: string, open, high, low, close, volume }` — timestamp is ISO string
- `WatchlistItem`: `{ id, ticker, company_name, added_at, price?, change_percent? }`
- `Watchlist`: `{ id, name, user_id, items: WatchlistItem[], created_at, updated_at }`
- `formatPercent(value)` takes percentage directly (e.g. 5.23), NOT decimal (0.0523) — it divides by 100 internally

## Permissions issue
- Subagent subprocess sessions block Write and Bash tools
- Do NOT rely on subagents to write new files — TPM must create new files directly or resume with explicit permission grants
- Edit tool works fine in subagents for existing files

## Component patterns
- Client components that use router: must be `"use client"` + `useRouter()`
- Pages that use hooks must be `"use client"` — Next.js App Router pages are server components by default
- NavBar must be a separate client component imported into the server-rendered root layout
- Use `useEffect` + `useState` for data fetching (React Query available but not yet set up with QueryClientProvider)

## Files created in Sprint 2
- `src/components/search/StockSearch.tsx` + `index.ts`
- `src/components/layout/NavBar.tsx`
- `src/components/charts/PriceChart.tsx` (updated `index.ts`)
- `src/components/watchlist/WatchlistPanel.tsx` + `index.ts`
- Updated: `src/app/layout.tsx`, `src/app/dashboard/page.tsx`, `src/app/stock/[ticker]/page.tsx`
