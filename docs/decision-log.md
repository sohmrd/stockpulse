# Decision Log

This file records every significant technical decision made during StockPulse development. The TPM maintains this log. Entries are append-only — never delete or rewrite a past decision. If a decision is reversed, add a new entry referencing the original.

---

### DEC-001: Initial Tech Stack Selection
**Date**: 2026-03-15
**Context**: StockPulse needs a full-stack web application capable of serving real-time stock data, interactive charts, and AI-generated investment insights. The team needed to select a frontend framework, backend framework, database, AI integration approach, and deployment platform before development began.
**Decision**: Adopt the following stack:
- **Frontend**: Next.js 14+ (App Router), TypeScript, Tailwind CSS, shadcn/ui, Recharts
- **Backend**: Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0 (async), Alembic
- **Database**: PostgreSQL (Neon / Supabase for managed hosting)
- **Cache**: Redis (Upstash or Railway)
- **AI**: Anthropic Claude API via `anthropic` Python SDK; `claude-sonnet-4-20250514` for production, `claude-haiku-4-5-20251001` for lightweight tasks
- **Auth**: JWT (PyJWT) with optional OAuth via authlib
- **Market Data**: Alpha Vantage (primary, free tier); Polygon.io as backup
- **Deployment**: Vercel (frontend) + Railway or Fly.io (backend)
- **CI/CD**: GitHub Actions (separate jobs for frontend and backend)

**Alternatives considered**:
- *Express / Node.js backend*: Rejected in favor of FastAPI. FastAPI's Pydantic integration, async-first design, and automatic OpenAPI docs make it better suited for a data-heavy API with strict validation requirements. Python also gives native access to the Anthropic SDK and the broader data/finance ecosystem.
- *Django + DRF*: Rejected. More opinionated and heavier than needed for an API-only service. FastAPI's dependency injection and async support are better fits.
- *Prisma + Supabase client (frontend-to-DB)*: Rejected. Direct DB access from the frontend bypasses server-side validation and rate limiting. A dedicated API layer is necessary for security and for the Claude integration.
- *OpenAI GPT-4*: Rejected in favor of Claude. The project is built on the Anthropic platform; Claude's longer context window and stronger instruction-following make it better suited for structured financial analysis output.
- *MongoDB*: Rejected in favor of PostgreSQL. Stock/portfolio data is highly relational (users → portfolios → holdings → transactions). PostgreSQL's ACID guarantees and SQL query capabilities are a better fit.
- *tRPC*: Considered for type-safe frontend-backend communication. Rejected because the backend is Python — tRPC is TypeScript-only. OpenAPI-generated types are the preferred approach for type safety across the language boundary.

**Rationale**:
- Next.js App Router enables both server-side rendering (SEO for public pages) and client-side interactivity (charts, real-time updates) in one framework.
- FastAPI is purpose-built for high-performance async APIs with automatic validation and docs generation.
- PostgreSQL + SQLAlchemy async provides reliable relational data storage with full migration support via Alembic.
- Claude API is the specified AI provider; `claude-sonnet-4` provides the reasoning quality needed for credible financial trend analysis.
- Vercel + Railway offers fast time-to-deployment with sensible free/starter tiers for an MVP.
- GitHub Actions keeps CI close to the code with no additional tooling dependencies.

**Consequences**:
- Frontend is TypeScript; backend is Python. The API contract layer (`docs/api-contracts/`) is the primary integration point and must be kept up to date.
- All database schema changes must go through Alembic migrations — no manual schema edits.
- The `CLAUDE_ENABLED` kill switch must be respected in all Claude API call sites so AI features can be disabled without redeployment.
- Market Data provider can be swapped (Alpha Vantage → Polygon → Finnhub) via the `MARKET_DATA_PROVIDER` env var; the `MarketDataService` abstraction in the backend must honor this.

---

### DEC-002: Monorepo Structure
**Date**: 2026-03-15
**Context**: The project has two independently deployable services (Next.js frontend, FastAPI backend) and shared assets (prompt templates, API contract definitions). A decision was needed on repository topology.
**Decision**: Use a **single GitHub monorepo** with two packages (`frontend/`, `backend/`) and shared top-level directories (`prompts/`, `docs/`, `.github/`).
**Alternatives considered**:
- *Two separate repositories (polyrepo)*: Simpler per-repo CI setup, but makes it harder to keep API contracts, prompt templates, and documentation in sync. Cross-repo PRs are awkward to review atomically.
- *Nx or Turborepo monorepo tooling*: Provides incremental builds and caching across workspaces. Rejected for now due to setup overhead at MVP stage. Can be adopted later if build times become a bottleneck.

**Rationale**: A monorepo simplifies atomic changes that span frontend and backend (e.g., a new endpoint + the UI that calls it). Path-filtered GitHub Actions jobs (`paths:` triggers) ensure frontend changes do not trigger backend CI and vice versa, preserving the independence benefit of a polyrepo approach.

**Consequences**:
- Each package maintains its own `package.json` / `pyproject.toml` and is independently deployable.
- CI workflows use `paths:` filters to avoid unnecessary job runs.
- The `prompts/` directory is shared between the backend (which loads templates at runtime) and documentation. The backend Dockerfile must copy `prompts/` into the image.
- If the monorepo grows to include additional services, introduce a monorepo tool (Turborepo or Nx) at that point.

---
