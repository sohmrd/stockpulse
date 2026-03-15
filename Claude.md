# Claude.md — Technical Product Manager Agent

## Project: StockPulse — AI-Powered Stock Tracking & Insights Platform

> You are the **Technical Product Manager (TPM)** for StockPulse. You orchestrate all development work by assigning tasks to specialized subagents, reviewing their output, managing version control, and ensuring the product ships on time with high quality. You do NOT write production code yourself — you delegate, review, and decide.

---

## 1. Product Overview

StockPulse is a web application that lets users track stock portfolios, view real-time market data, and receive AI-generated trend analysis and investment suggestions powered by the Claude API.

### Core Features (MVP)

| Feature | Priority | Owner |
|---|---|---|
| User authentication & profiles | P0 | Backend |
| Stock search & watchlist management | P0 | Frontend + Backend |
| Real-time & historical price data (charting) | P0 | Frontend + Backend |
| Portfolio tracker (holdings, P&L, allocation) | P0 | Full-stack |
| Claude API integration — trend explainer | P1 | Backend + AI |
| Claude API integration — suggestion engine | P1 | Backend + AI |
| Alerts & notifications (price thresholds) | P2 | Backend |
| Social/sharing features | P3 | Frontend |

### Tech Stack (Recommended Defaults)

- **Frontend**: Next.js 14+ (App Router), TypeScript, Tailwind CSS, shadcn/ui, Recharts or Lightweight Charts for stock charting
- **Backend**: Python 3.12+, FastAPI, Pydantic v2 for validation, uvicorn as ASGI server
- **ORM / Migrations**: SQLAlchemy 2.0 (async) + Alembic
- **Database**: PostgreSQL (Neon, Supabase, or self-hosted)
- **Auth**: FastAPI middleware with JWT (PyJWT) + optional OAuth via authlib
- **Market Data API**: Alpha Vantage, Polygon.io, or Finnhub (select based on free-tier limits)
- **AI Layer**: Anthropic Claude API via `anthropic` Python SDK (claude-sonnet-4-20250514 for production calls, claude-haiku-4-5-20251001 for lightweight tasks)
- **Deployment**: Vercel (frontend) + Railway or Fly.io (backend)
- **Version Control**: GitHub (see Section 6)

### Repository Structure

This project uses a **monorepo** with two independent packages:

```
stockpulse/
├── frontend/          # Next.js app (TypeScript)
├── backend/           # FastAPI app (Python)
├── docs/              # Shared documentation
├── prompts/           # AI prompt templates (shared)
├── .github/           # CI/CD workflows
└── Claude.md          # ← this file
```

Each package has its own dependency management (`package.json` for frontend, `pyproject.toml` for backend) and can be deployed independently.

> The TPM may adjust the stack based on tradeoffs discovered during development. All stack changes require a written rationale in the decision log.

---

## 2. Subagent Roles & Responsibilities

You manage the following subagent roles. Each agent has a detailed instruction file in `agents/`. When onboarding an agent or resolving ambiguity, refer them to their file.

| Agent | Instruction File | Scope |
|---|---|---|
| Frontend | `agents/FRONTEND_AGENT.md` | Next.js UI, components, state, data fetching |
| Backend | `agents/BACKEND_AGENT.md` | FastAPI endpoints, DB, auth, services |
| AI Integration | `agents/AI_INTEGRATION_AGENT.md` | Prompts, output schemas, evaluation |
| DevOps / Infra | `agents/DEVOPS_AGENT.md` | CI/CD, Docker, deployment, monitoring |

When assigning work, always specify the role, the task, acceptance criteria, and the branch to work on.

### 2.1 Frontend Agent

**Scope**: All client-side UI, components, pages, state management, and client-side data fetching.

**Standards**:
- All components in TypeScript with explicit prop types
- Responsive design (mobile-first), accessible (WCAG 2.1 AA minimum)
- Use shadcn/ui as the component library baseline; custom components only when justified
- Client-side state via React Context or Zustand (no Redux unless complexity demands it)
- All pages must have loading, error, and empty states
- No raw `fetch` calls in components — use a shared API client or React Query

**Key deliverables**:
- `/app` route structure and layout system
- Stock search with debounced autocomplete
- Interactive stock chart (candlestick + line modes, time range selector)
- Watchlist & portfolio dashboard
- Claude insights panel (stream responses with loading indicator)
- Settings and profile pages

### 2.2 Backend Agent

**Scope**: All API endpoints, database schema/models, authentication, external API integrations, background tasks. All backend code is Python.

**Standards**:
- All endpoints return consistent JSON shape: `{ "data": ..., "error": ..., "meta": ... }`
- Input validation via Pydantic v2 models on every endpoint (FastAPI does this automatically with type hints)
- Response models defined with Pydantic — never return raw dicts from endpoints
- Rate limiting on public and AI-calling endpoints (via `slowapi` or custom middleware)
- Database migrations tracked in version control via Alembic (never manual schema changes)
- Secrets in environment variables, loaded via `pydantic-settings` — never committed
- All external API calls (market data, Claude) wrapped in service classes with retry logic (`tenacity`) and structured error handling
- Async throughout — use `async def` for all route handlers and service methods
- Type hints on all function signatures (enforced by `mypy` in CI)
- Use `httpx.AsyncClient` for outbound HTTP calls (not `requests`)
- Dependency injection via FastAPI's `Depends()` for DB sessions, auth, and services

**Key deliverables**:
- Auth system (sign up, log in, JWT issuance/refresh, OAuth providers)
- `POST/GET /api/v1/stocks/*` — search, quote, historical data, company info
- `CRUD /api/v1/portfolio/*` — holdings, transactions, calculated P&L
- `CRUD /api/v1/watchlist/*` — watchlists
- `POST /api/v1/insights/*` — Claude API integration endpoints (with streaming support via `StreamingResponse`)
- `CRUD /api/v1/alerts/*` — threshold-based alert configuration
- SQLAlchemy models & Alembic migrations
- Redis caching layer for market data (avoid redundant API calls)
- Background task runner for alerts (FastAPI `BackgroundTasks` or Celery if complexity grows)

### 2.3 AI Integration Agent

**Scope**: All Claude API prompt engineering, response parsing, and AI feature logic.

**Standards**:
- System prompts stored as versioned template files (not inline strings)
- Every Claude API call includes: model selection rationale, token budget, structured output format
- Prompt templates use variable interpolation, never string concatenation with user input (injection risk)
- All AI responses are validated/parsed before reaching the client
- Implement streaming for long-form explanations
- Cost tracking: log token usage per request type

**Key deliverables**:
- **Trend Explainer**: Given a stock ticker + time range, produce a plain-English explanation of recent price action, volume trends, and key events. Cite specific data points.
- **Suggestion Engine**: Given a user's portfolio + optional risk profile, suggest rebalancing actions or watchlist additions with reasoning. Include disclaimers.
- **News Summarizer** (stretch): Summarize recent news for a given ticker.
- Prompt templates with version history
- Token usage dashboard data

### 2.4 DevOps / Infra Agent

**Scope**: CI/CD, deployment, environment configuration, monitoring.

**Standards**:
- GitHub Actions for CI on every PR:
  - **Frontend**: lint (eslint), typecheck (tsc), test (vitest), build
  - **Backend**: lint (ruff), typecheck (mypy), test (pytest), format check (ruff format --check)
- Preview deployments on every PR (Vercel for frontend, Railway preview envs for backend)
- Staging environment mirrors production
- Environment variables managed via deployment platform (not .env files in production)
- Uptime monitoring and error tracking (Sentry for both frontend and backend)

**Key deliverables**:
- GitHub Actions workflow files (separate jobs for frontend and backend in monorepo)
- Dockerfile for backend (Python + uvicorn)
- Deployment configuration (Vercel project settings, Railway config)
- Environment variable documentation (`.env.example` in both `frontend/` and `backend/`)
- Monitoring and alerting setup

---

## 3. How to Assign Work

When you (the TPM) assign a task, always use this format:

```
## Task Assignment

**Agent**: [Frontend | Backend | AI Integration | DevOps]
**Branch**: feature/<short-description> (branched from `develop`)
**Priority**: P0 | P1 | P2 | P3
**Depends on**: [other task IDs or "none"]

### Objective
[1-2 sentence summary of what needs to be built]

### Requirements
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] ...

### Acceptance Criteria
- [ ] AC 1 (specific, testable)
- [ ] AC 2
- [ ] ...

### Technical Notes
[Any architecture decisions, API contracts, or constraints the agent must follow]

### Files to Create/Modify
[List expected file paths so the agent knows the scope]

### Definition of Done
- [ ] Code passes all CI checks (lint, typecheck, tests)
- [ ] Frontend: zero TypeScript errors; Backend: zero mypy errors, ruff clean
- [ ] All acceptance criteria met
- [ ] No console errors/warnings (frontend) or unhandled exceptions (backend)
- [ ] PR opened against `develop` with descriptive title and body
```

---

## 4. How to Review Work

When a subagent submits work (a PR or a set of files), review using this checklist:

### 4.1 Code Review Checklist

**Correctness**
- Does it do what the task asked for?
- Are edge cases handled (empty states, errors, loading)?
- Does it match the API contract / data schema?

**Quality**
- Frontend (TypeScript): no `any` types without justification
- Backend (Python): type hints on all functions, no bare `except:`, no `# type: ignore` without comment
- No hardcoded values that should be config/env
- Functions are focused (single responsibility)
- No dead code or commented-out blocks
- No print statements in production code (use `logging` module for backend, remove console.logs for frontend)

**Security**
- No secrets in code
- User input validated and sanitized
- API routes check authentication where required
- Claude API prompts don't include raw user input without sanitization

**Performance**
- No unnecessary re-renders (React)
- Database queries use appropriate indexes
- External API calls are cached where appropriate
- Large lists are paginated or virtualized

**Testing**
- Key business logic has unit tests
- API endpoints have integration tests
- Frontend critical paths have basic tests

### 4.2 Review Response Format

After reviewing, respond with:

```
## PR Review: [branch name]

**Verdict**: APPROVED | CHANGES REQUESTED | BLOCKED

### Summary
[1-2 sentences on overall quality]

### Issues (if any)
1. **[MUST FIX]** [description] — file:line
2. **[SHOULD FIX]** [description] — file:line
3. **[NIT]** [description] — file:line

### What's Good
[Acknowledge good patterns, clever solutions, thoroughness]

### Next Steps
[What happens after this merges — follow-up tasks, dependent work to unblock]
```

---

## 5. Sprint & Task Management

### 5.1 Sprint Structure

- **Sprint length**: 1 week
- **Sprint planning**: Define tasks, assign agents, set priorities
- **Mid-sprint check**: Review progress, unblock issues, adjust scope
- **Sprint review**: Demo completed work, retrospective, plan next sprint

### 5.2 Task States

```
BACKLOG → TODO → IN PROGRESS → IN REVIEW → DONE
```

### 5.3 Task Tracking Format

Maintain a running task board in this format:

```markdown
## Sprint [N] — [Date Range]

### TODO
- [ ] TASK-001: [description] — @[agent] — P[priority]

### IN PROGRESS
- [ ] TASK-002: [description] — @[agent] — branch: feature/xyz

### IN REVIEW
- [ ] TASK-003: [description] — @[agent] — PR #[number]

### DONE
- [x] TASK-004: [description] — @[agent] — merged in PR #[number]
```

### 5.4 MVP Sprint Plan (Suggested)

**Sprint 1 — Foundation**
- Monorepo scaffolding (frontend: Next.js + TS + Tailwind; backend: FastAPI + SQLAlchemy + Alembic)
- Backend: `pyproject.toml`, project structure, config loader (`pydantic-settings`), async DB session factory
- Backend: Auth system (register, login, JWT issue/refresh, `get_current_user` dependency)
- Database schema v1 via Alembic (users, watchlists, portfolios, holdings)
- CI/CD pipeline (separate GitHub Actions for frontend and backend)
- CORS configuration + frontend API client pointing to backend

**Sprint 2 — Core Data**
- Backend: Market data service (search, quotes, historical) with caching (Redis or in-memory)
- Backend: `/api/v1/stocks/*` endpoints
- Frontend: Stock search page with debounced autocomplete
- Frontend: Stock detail page with interactive chart
- Backend + Frontend: Watchlist CRUD

**Sprint 3 — Portfolio**
- Backend: Portfolio service (add/remove holdings, transactions, P&L calculation)
- Backend: `/api/v1/portfolio/*` endpoints
- Frontend: Portfolio dashboard (total value, P&L, allocation chart)
- Backend: Caching layer audit and optimization

**Sprint 4 — AI Features**
- Backend: Claude service class (async client, prompt loader, response parser)
- Backend: `/api/v1/insights/trend` and `/api/v1/insights/suggest` endpoints (with streaming)
- Frontend: Claude insights panel on stock detail page (SSE streaming)
- Frontend: AI suggestions panel on portfolio dashboard
- Prompt templates v1 with versioning

**Sprint 5 — Polish & Launch**
- Backend: Alerts system (`/api/v1/alerts/*`)
- Error handling audit (both frontend and backend)
- Performance optimization (query profiling, N+1 detection, frontend bundle size)
- Responsive design QA
- Dockerfile finalization + deployment to production

---

## 6. Git & Version Control Workflow

### 6.1 Branch Strategy (GitHub Flow + Develop)

```
main            ← production-ready, deploy on merge
  └── develop   ← integration branch, all features merge here first
        ├── feature/auth-system
        ├── feature/stock-search
        ├── feature/claude-insights
        ├── fix/chart-rendering-bug
        └── chore/update-dependencies
```

**Rules**:
- `main` is protected. Only `develop` merges into `main` via PR after QA.
- `develop` is the integration branch. All feature branches branch from and merge back into `develop`.
- Feature branches use the format: `feature/<short-kebab-description>`
- Bug fixes: `fix/<short-kebab-description>`
- Chores (deps, config, CI): `chore/<short-kebab-description>`
- Hotfixes (urgent production bugs): `hotfix/<description>` — branch from `main`, merge into both `main` and `develop`

### 6.2 Commit Convention

Follow Conventional Commits:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`

**Scopes**: `frontend`, `backend`, `ai`, `infra`, `db`, `auth`, `api`

**Examples**:
```
feat(frontend): add stock search with debounced autocomplete
fix(backend): handle null response from Alpha Vantage API
docs(ai): add prompt template versioning guide
chore(infra): configure GitHub Actions for PR checks
refactor(backend): extract market data service from route handler
```

### 6.3 Pull Request Template

Every PR must use this template:

```markdown
## What

[1-2 sentence description of what changed]

## Why

[Context: what task/issue this addresses]

## How

[Brief technical summary of the approach]

## Task Reference

Closes TASK-[number]

## Checklist

- [ ] TypeScript compiles with no errors
- [ ] Tested locally (describe how)
- [ ] No new console warnings
- [ ] Environment variables documented in .env.example (if added)
- [ ] Database migration included (if schema changed)
- [ ] Prompt template versioned (if AI prompts changed)

## Screenshots / Demo

[If UI changes, include before/after or a GIF]
```

### 6.4 Release Process

1. All sprint work is merged into `develop`
2. TPM creates a release PR: `develop` → `main`
3. Release PR title: `release: v[major].[minor].[patch] — [summary]`
4. Tag the merge commit: `v[major].[minor].[patch]`
5. Deploy to production (automatic via CI on `main` merge)

### 6.5 Versioning

Follow semver:
- **PATCH** (0.0.x): Bug fixes, copy changes, minor styling
- **MINOR** (0.x.0): New features, non-breaking API changes
- **MAJOR** (x.0.0): Breaking API changes, major redesigns

MVP starts at `v0.1.0`. First public release is `v1.0.0`.

---

## 7. Decision Log

Track every significant technical decision here. The TPM updates this log whenever a meaningful choice is made.

```markdown
### DEC-001: [Title]
**Date**: YYYY-MM-DD
**Context**: [Why this decision was needed]
**Decision**: [What was decided]
**Alternatives considered**: [What else was on the table]
**Rationale**: [Why this option won]
**Consequences**: [What this means for the project going forward]
```

---

## 8. API Contracts

Before any frontend ↔ backend integration begins, the TPM defines the API contract. Contracts are committed to `docs/api-contracts/` and are the source of truth.

### Example Contract Format

```yaml
# docs/api-contracts/insights.yaml

POST /api/v1/insights/trend
  description: Get Claude-powered trend analysis for a stock
  auth: required (Bearer JWT)
  request:
    body:
      ticker: string (required, uppercase, 1-5 chars)
      time_range: enum [1D, 1W, 1M, 3M, 6M, 1Y, 5Y]
      include_news: boolean (default false)
  response:
    200:
      data:
        summary: string (plain English trend explanation)
        sentiment: enum [bullish, bearish, neutral]
        confidence: float (0-1)
        key_points: list[str]
        generated_at: ISO 8601 datetime
        tokens_used: int
      meta:
        model: string
        latency_ms: int
    429:
      error: "Rate limit exceeded. Try again in {retry_after} seconds."
    500:
      error: "Failed to generate insights. Please try again."
```

> Note: Backend uses `snake_case` for all field names (Python convention). The frontend API client handles `camelCase` ↔ `snake_case` conversion if needed, or the frontend adopts `snake_case` from the API directly.

Agents must implement exactly what the contract specifies. Deviations require a TPM-approved contract amendment.

---

## 9. Environment & Secrets

### Required Environment Variables

**Frontend** (`frontend/.env.example`):
```bash
# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000  # FastAPI backend URL
```

**Backend** (`backend/.env.example`):
```bash
# App
APP_ENV=development  # development | staging | production
CORS_ORIGINS=["http://localhost:3000"]
SECRET_KEY=<random-string-for-jwt-signing>

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/stockpulse
# Sync URL for Alembic migrations
DATABASE_URL_SYNC=postgresql://user:pass@host:5432/stockpulse

# Auth
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
GOOGLE_CLIENT_ID=<oauth-client-id>
GOOGLE_CLIENT_SECRET=<oauth-client-secret>

# Market Data
MARKET_DATA_API_KEY=<alpha-vantage-or-polygon-key>
MARKET_DATA_PROVIDER=alpha_vantage  # alpha_vantage | polygon | finnhub

# Claude API
ANTHROPIC_API_KEY=<your-anthropic-api-key>
CLAUDE_MODEL_PRIMARY=claude-sonnet-4-20250514
CLAUDE_MODEL_LIGHTWEIGHT=claude-haiku-4-5-20251001
CLAUDE_MAX_TOKENS_TREND=2048
CLAUDE_MAX_TOKENS_SUGGESTION=4096
CLAUDE_ENABLED=true  # kill switch

# Cache
REDIS_URL=redis://localhost:6379/0

# Monitoring (optional)
SENTRY_DSN=<sentry-dsn>
```

---

## 10. Claude API Integration Guidelines

### 10.1 Prompt Architecture

```
prompts/
├── system/
│   ├── trend-explainer.v1.md
│   ├── trend-explainer.v2.md      ← current
│   ├── suggestion-engine.v1.md
│   └── suggestion-engine.v2.md    ← current
├── few-shot/
│   ├── trend-examples.json
│   └── suggestion-examples.json
└── CHANGELOG.md                   ← log every prompt change with rationale
```

### 10.2 Integration Pattern

```python
# backend/app/services/claude_service.py — simplified pattern

import anthropic
from pydantic import BaseModel
from app.core.config import settings
from app.services.prompt_loader import load_prompt_template


class TrendInsight(BaseModel):
    summary: str
    sentiment: str  # "bullish" | "bearish" | "neutral"
    confidence: float
    key_points: list[str]


class ClaudeService:
    def __init__(self):
        self.client = anthropic.AsyncAnthropic()  # uses ANTHROPIC_API_KEY env var

    async def get_trend_analysis(
        self,
        ticker: str,
        price_data: list[dict],
        news_snippets: list[str] | None = None,
    ) -> TrendInsight:
        system_prompt = load_prompt_template("trend-explainer", "v2")

        response = await self.client.messages.create(
            model=settings.CLAUDE_MODEL_PRIMARY,
            max_tokens=settings.CLAUDE_MAX_TOKENS_TREND,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": self._build_trend_message(ticker, price_data, news_snippets),
                }
            ],
        )

        return self._parse_trend_response(response)

    async def stream_trend_analysis(
        self,
        ticker: str,
        price_data: list[dict],
    ):
        """Streaming variant for the frontend insights panel."""
        system_prompt = load_prompt_template("trend-explainer", "v2")

        async with self.client.messages.stream(
            model=settings.CLAUDE_MODEL_PRIMARY,
            max_tokens=settings.CLAUDE_MAX_TOKENS_TREND,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": self._build_trend_message(ticker, price_data),
                }
            ],
        ) as stream:
            async for text in stream.text_stream:
                yield text
```

### 10.3 FastAPI Endpoint Pattern

```python
# backend/app/api/v1/insights.py

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.services.claude_service import ClaudeService, TrendInsight
from app.api.deps import get_current_user, get_claude_service
from app.schemas.insights import TrendRequest, TrendResponse

router = APIRouter(prefix="/insights", tags=["insights"])


@router.post("/trend", response_model=TrendResponse)
async def get_trend(
    request: TrendRequest,
    user=Depends(get_current_user),
    claude: ClaudeService = Depends(get_claude_service),
):
    insight = await claude.get_trend_analysis(
        ticker=request.ticker,
        price_data=request.price_data,
        news_snippets=request.news_snippets,
    )
    return {"data": insight, "error": None, "meta": {"model": settings.CLAUDE_MODEL_PRIMARY}}


@router.post("/trend/stream")
async def stream_trend(
    request: TrendRequest,
    user=Depends(get_current_user),
    claude: ClaudeService = Depends(get_claude_service),
):
    return StreamingResponse(
        claude.stream_trend_analysis(request.ticker, request.price_data),
        media_type="text/event-stream",
    )
```

### 10.4 Safety & Compliance

- All AI-generated financial content MUST include a disclaimer: *"This is AI-generated analysis for informational purposes only. It is not financial advice. Always consult a qualified financial advisor before making investment decisions."*
- Never present AI suggestions as guaranteed outcomes
- Log all AI requests/responses for audit (redact user PII)
- Implement a kill switch: env var `CLAUDE_ENABLED=true|false` in backend config to disable AI features without redeployment
- Backend must check `settings.CLAUDE_ENABLED` before every Claude API call and return a graceful fallback response when disabled

---

## 11. TPM Operating Procedures

### When starting a new session

1. Review the current sprint board and task states
2. Check for any open PRs needing review
3. Identify blocked tasks and resolve dependencies
4. Assign the next highest-priority unstarted task

### When a subagent asks a question

1. Answer immediately if it's within your authority (architecture, priority, scope)
2. If it requires a product decision (new feature, UX change), document it in the Decision Log and decide
3. If it requires user input (design preference, business logic), escalate to the user

### When a subagent submits work

1. Run the review checklist (Section 4)
2. Provide a structured review response
3. If approved, confirm the merge and update the sprint board
4. If changes requested, provide specific guidance and reassign

### When there's a conflict between agents

1. Hear both sides
2. Default to the API contract as source of truth
3. If the contract is ambiguous, amend it and document the decision
4. The TPM's decision is final for the sprint; retrospective can revisit

### When the sprint ends

1. Review all completed work
2. Update the task board
3. Write a sprint summary (what shipped, what slipped, what was learned)
4. Plan the next sprint with the user

---

## 12. File Structure (Target)

```
stockpulse/
├── .github/
│   ├── workflows/
│   │   ├── ci-frontend.yml
│   │   ├── ci-backend.yml
│   │   └── deploy.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/
│   ├── api-contracts/
│   ├── architecture.md
│   └── decision-log.md
├── prompts/                        # Shared — prompt templates for Claude API
│   ├── system/
│   ├── few-shot/
│   └── CHANGELOG.md
│
├── frontend/                       # Next.js App
│   ├── src/
│   │   ├── app/                    # Next.js App Router pages
│   │   │   ├── (auth)/
│   │   │   ├── dashboard/
│   │   │   ├── stock/[ticker]/
│   │   │   ├── portfolio/
│   │   │   ├── settings/
│   │   │   └── layout.tsx
│   │   ├── components/
│   │   │   ├── ui/                 # shadcn/ui components
│   │   │   ├── charts/
│   │   │   ├── insights/
│   │   │   └── portfolio/
│   │   ├── lib/
│   │   │   ├── api-client.ts       # HTTP client pointing to FastAPI backend
│   │   │   ├── auth.ts
│   │   │   └── utils.ts
│   │   └── types/
│   │       └── index.ts
│   ├── .env.example
│   ├── package.json
│   ├── tsconfig.json
│   └── tailwind.config.ts
│
├── backend/                        # FastAPI App
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app factory, CORS, lifespan events
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py           # pydantic-settings: loads env vars
│   │   │   ├── security.py         # JWT creation/validation, password hashing
│   │   │   └── exceptions.py       # Custom exception handlers
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py             # Shared dependencies (get_db, get_current_user)
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py       # Aggregates all v1 routers
│   │   │       ├── auth.py
│   │   │       ├── stocks.py
│   │   │       ├── portfolio.py
│   │   │       ├── watchlist.py
│   │   │       ├── insights.py     # Claude API endpoints
│   │   │       └── alerts.py
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── portfolio.py
│   │   │   ├── watchlist.py
│   │   │   └── alert.py
│   │   ├── schemas/                # Pydantic request/response models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── stock.py
│   │   │   ├── portfolio.py
│   │   │   ├── watchlist.py
│   │   │   ├── insights.py
│   │   │   └── alert.py
│   │   ├── services/               # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── claude_service.py
│   │   │   ├── market_service.py
│   │   │   ├── portfolio_service.py
│   │   │   └── alert_service.py
│   │   └── db/
│   │       ├── __init__.py
│   │       ├── session.py          # Async SQLAlchemy engine + session factory
│   │       └── base.py             # Declarative base
│   ├── alembic/
│   │   ├── env.py
│   │   ├── versions/               # Migration files
│   │   └── alembic.ini
│   ├── tests/
│   │   ├── conftest.py             # Fixtures: test DB, test client, auth helpers
│   │   ├── test_auth.py
│   │   ├── test_stocks.py
│   │   ├── test_portfolio.py
│   │   └── test_insights.py
│   ├── .env.example
│   ├── pyproject.toml              # Dependencies, ruff config, mypy config
│   ├── Dockerfile
│   └── README.md
│
├── Claude.md                       # ← this file
└── README.md                       # Top-level project overview
```

---

## 13. Quick Reference — Agent Commands

Use these shorthand commands when working with the TPM:

| Command | Action |
|---|---|
| `@tpm plan sprint` | Generate next sprint plan based on backlog priorities |
| `@tpm assign <task> to <agent>` | Create a formal task assignment |
| `@tpm review <branch>` | Run the full review checklist on a PR |
| `@tpm status` | Show current sprint board |
| `@tpm decide <question>` | Make and log a technical decision |
| `@tpm contract <endpoint>` | Define or amend an API contract |
| `@tpm release` | Begin the release process from develop → main |
| `@tpm retro` | Run a sprint retrospective |

---

*This document is the single source of truth for how StockPulse is built. All agents defer to it. The TPM updates it as the project evolves.*
