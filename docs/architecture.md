# StockPulse — Architecture Overview

## 1. System Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                         Client Browser                           │
│                    (Next.js 14 App Router)                       │
└────────────────────────────┬─────────────────────────────────────┘
                             │ HTTPS (REST + SSE streaming)
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                     FastAPI Backend                               │
│                  (Python 3.12, uvicorn)                          │
│                                                                   │
│  ┌───────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ Auth API  │  │  Stocks API  │  │     Insights API         │  │
│  │ /auth/*   │  │ /stocks/*    │  │ /insights/trend          │  │
│  └───────────┘  └──────┬───────┘  │ /insights/suggest        │  │
│                         │         └──────────┬───────────────┘  │
│  ┌────────────────────┐ │                    │                   │
│  │   Portfolio API    │ │         ┌──────────▼───────────────┐  │
│  │   /portfolio/*     │ │         │      Claude Service       │  │
│  └────────────────────┘ │         │  (anthropic Python SDK)  │  │
│                          │         └──────────┬───────────────┘  │
│  ┌────────────────────┐ │                    │                   │
│  │   Watchlist API    │ │                    │ Anthropic API     │
│  │   /watchlist/*     │ │                    │ (claude-sonnet-4) │
│  └────────────────────┘ │         ┌──────────▼───────────────┐  │
│                          │         │    prompts/ templates    │  │
│  ┌────────────────────┐ │         │    (versioned .md files) │  │
│  │    Alerts API      │ │         └──────────────────────────┘  │
│  │    /alerts/*       │ │                                        │
│  └────────────────────┘ │                                        │
│                          │                                        │
│  ┌──────────────────────▼────────────┐                           │
│  │         Market Data Service       │                           │
│  │  (Alpha Vantage / Polygon / Finn) │                           │
│  └──────────────────────┬────────────┘                           │
│                          │                                        │
└──────────────────────────┼────────────────────────────────────── ┘
                           │
              ┌────────────┴─────────────┐
              │                          │
   ┌──────────▼──────────┐   ┌──────────▼──────────┐
   │     PostgreSQL       │   │        Redis         │
   │ (Neon / Supabase)   │   │  (Upstash / Railway) │
   │                      │   │  Market data cache   │
   │  users               │   │  Rate limit counters │
   │  portfolios          │   └─────────────────────┘
   │  holdings            │
   │  watchlists          │
   │  alerts              │
   └─────────────────────┘
```

## 2. Repository Structure

StockPulse is a **monorepo** with two independently deployable packages:

```
stockpulse/
├── frontend/          # Next.js 14 (TypeScript) — deployed to Vercel
├── backend/           # FastAPI (Python 3.12) — deployed to Railway / Fly.io
├── prompts/           # Versioned Claude prompt templates (shared)
├── docs/              # Architecture, API contracts, decision log
├── .github/           # CI/CD workflows (GitHub Actions)
└── Claude.md          # TPM instructions and project source of truth
```

Each package has its own dependency manifest and can be built, tested, and deployed independently. CI jobs are path-filtered so a change in `frontend/` never triggers backend CI and vice versa.

## 3. Frontend

- **Framework**: Next.js 14+ with App Router (file-based routing in `app/`)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS + shadcn/ui component library
- **Charting**: Recharts or Lightweight Charts (TradingView)
- **State**: React Context for auth/user state; React Query (TanStack Query) for server state
- **API Client**: Shared `lib/api-client.ts` — all backend calls go through this; no raw `fetch` in components
- **Deployment**: Vercel (automatic preview deployments on PRs, production on `main` merge)

### Key Pages

| Route | Description |
|---|---|
| `/` | Landing / marketing |
| `/(auth)/login` | Authentication |
| `/(auth)/register` | Registration |
| `/dashboard` | Portfolio overview + watchlist |
| `/stock/[ticker]` | Stock detail + chart + Claude insights |
| `/portfolio` | Full portfolio view (holdings, P&L, allocation) |
| `/settings` | User profile and preferences |

## 4. Backend

- **Framework**: FastAPI (async throughout)
- **Language**: Python 3.12+
- **Validation**: Pydantic v2 on all request/response models
- **ORM**: SQLAlchemy 2.0 (async) with Alembic migrations
- **Auth**: JWT (PyJWT) issued on login; `get_current_user` FastAPI dependency guards protected routes
- **External HTTP**: `httpx.AsyncClient` with `tenacity` retry logic
- **Caching**: Redis for market data (TTL: 60s for quotes, 24h for company info)
- **Rate Limiting**: `slowapi` on public endpoints and all Claude-calling endpoints
- **Deployment**: Railway or Fly.io (Dockerfile in `backend/`)

### API Versioning

All endpoints are prefixed `/api/v1/`. A new version prefix (`/api/v2/`) will be introduced only for breaking changes.

### Response Envelope

```json
{
  "data": {},
  "error": null,
  "meta": {}
}
```

## 5. AI Integration (Claude API)

- **SDK**: `anthropic` Python SDK (async client)
- **Models**:
  - `claude-sonnet-4-20250514` — primary (trend analysis, suggestions)
  - `claude-haiku-4-5-20251001` — lightweight tasks (quick summaries, classification)
- **Prompts**: Stored as versioned Markdown templates in `prompts/system/`. Loaded at runtime by `PromptLoader` service. Never hardcoded inline.
- **Streaming**: Long-form insights use `StreamingResponse` (SSE) from FastAPI; frontend consumes via `EventSource` or `fetch` with `ReadableStream`.
- **Kill Switch**: `CLAUDE_ENABLED` env var — set to `false` to disable all AI features without redeployment.
- **Cost Control**: Token budgets per request type; usage logged per request.
- **Safety**: All AI financial content includes a mandatory disclaimer. User input is never interpolated directly into prompts.

## 6. Data Flow — Stock Insight Request

```
User clicks "Analyze" on /stock/AAPL
       │
       ▼
Frontend POSTs to /api/v1/insights/trend/stream
       │
       ▼
Backend: verify JWT → validate request → check CLAUDE_ENABLED
       │
       ▼
MarketService: fetch recent OHLCV data for AAPL (from cache or Alpha Vantage)
       │
       ▼
PromptLoader: load prompts/system/trend-explainer.v2.md, interpolate variables
       │
       ▼
ClaudeService: stream response from Anthropic API
       │
       ▼
FastAPI StreamingResponse (text/event-stream) → Frontend EventSource
       │
       ▼
Frontend renders streaming text in Claude insights panel
```

## 7. CI/CD

See `.github/workflows/` for full pipeline definitions.

| Trigger | Action |
|---|---|
| PR opened/updated | CI checks (lint, typecheck, test, build) for changed packages |
| Merge to `develop` | Deploy to staging |
| Merge to `main` | Deploy to production + create Git tag |
| Manual dispatch | Force deploy to any environment |

## 8. Environments

| Environment | Branch | Backend URL | Frontend URL |
|---|---|---|---|
| Local | any | `localhost:8000` | `localhost:3000` |
| Staging | `develop` | `api-staging.stockpulse.app` | `staging.stockpulse.app` |
| Production | `main` | `api.stockpulse.app` | `stockpulse.app` |

## 9. Security

- HTTPS enforced on all production endpoints (deployment platform handles TLS)
- CORS restricted to allowed origins per environment (no `*` in production)
- Rate limiting on all public and AI-calling endpoints
- JWT secret rotated per environment
- Secrets managed via deployment platform env vars — never in `.env` files or Docker images
- Security headers: `X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`
- Dependabot enabled for both `frontend/` and `backend/`
