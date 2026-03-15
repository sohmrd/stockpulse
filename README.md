# StockPulse

**AI-powered stock tracking and investment insights — built for everyday investors.**

StockPulse lets you track your portfolio, monitor stocks you care about, and get plain-English explanations of market trends powered by Claude AI. No finance degree required.

---

## What It Does

| Feature | Description |
|---|---|
| **Portfolio Tracker** | Add your holdings and see your total value, profit/loss, and allocation — updated in real time |
| **Stock Search & Watchlist** | Search any ticker, view historical price charts, and save stocks to a personal watchlist |
| **AI Trend Explainer** | Ask "what happened to this stock?" and get a clear, human-readable summary of recent price action |
| **AI Suggestion Engine** | Get rebalancing ideas based on your portfolio and risk preferences, with plain-English reasoning |
| **Price Alerts** | Set a target price and get notified when a stock crosses it |

> **Disclaimer:** AI-generated analysis is for informational purposes only. It is not financial advice. Always consult a qualified financial advisor before making investment decisions.

---

## Screenshots

*Coming soon — the app is currently in active development (Sprint 1 complete).*

---

## How It Works

```
You → StockPulse Frontend (Next.js)
              ↓
      StockPulse Backend (FastAPI)
         ↙           ↘
  Market Data API    Claude AI (Anthropic)
  (live prices)      (trend analysis & suggestions)
              ↓
         PostgreSQL
         (your portfolio & watchlist data)
```

1. You interact with a fast, responsive web interface
2. The backend fetches real-time and historical stock prices from a market data provider
3. When you request AI insights, the backend sends relevant price data to Claude — **your portfolio data is never sent to Claude without your action**
4. All your personal data (holdings, watchlist, alerts) is stored securely in a private database

---

## Tech Stack

**Frontend**
- [Next.js 14](https://nextjs.org/) — React framework for fast, server-rendered pages
- [TypeScript](https://www.typescriptlang.org/) — type-safe JavaScript
- [Tailwind CSS](https://tailwindcss.com/) + [shadcn/ui](https://ui.shadcn.com/) — clean, accessible UI components
- [Recharts](https://recharts.org/) — interactive stock charts

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — high-performance Python API server
- [PostgreSQL](https://www.postgresql.org/) — relational database for user data
- [SQLAlchemy](https://www.sqlalchemy.org/) — database ORM with async support
- [JWT](https://jwt.io/) — secure authentication tokens

**AI**
- [Anthropic Claude API](https://www.anthropic.com/) — powers the trend explainer and suggestion engine
- `claude-sonnet-4` for deep analysis, `claude-haiku-4` for lightweight tasks

---

## Project Status

StockPulse is under active development. Here's where things stand:

| Sprint | Focus | Status |
|---|---|---|
| Sprint 1 — Foundation | Monorepo scaffold, auth system, database schema, CI/CD | **Complete** |
| Sprint 2 — Core Data | Market data service, stock search UI, watchlist, price charts | Upcoming |
| Sprint 3 — Portfolio | Holdings tracker, P&L calculation, allocation dashboard | Backlog |
| Sprint 4 — AI Features | Claude trend explainer, suggestion engine, streaming UI | Backlog |
| Sprint 5 — Polish | Alerts, error handling, performance, production deployment | Backlog |

---

## Repository Structure

```
stockpulse/
├── frontend/          # Next.js web application (TypeScript)
├── backend/           # FastAPI REST API (Python)
├── docs/              # Architecture docs and API contracts
├── prompts/           # Claude AI prompt templates (versioned)
└── .github/           # CI/CD workflows (GitHub Actions)
```

The frontend and backend are independent — they communicate over a REST API and can be deployed separately.

---

## Getting Started (Local Development)

### Prerequisites

- [Node.js 20+](https://nodejs.org/)
- [Python 3.12+](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/) (or a free hosted instance via [Neon](https://neon.tech/) or [Supabase](https://supabase.com/))
- An [Anthropic API key](https://console.anthropic.com/) for AI features
- A market data API key ([Alpha Vantage](https://www.alphavantage.co/) has a free tier)

### 1. Clone the repo

```bash
git clone https://github.com/sohmrd/stockpulse.git
cd stockpulse
```

### 2. Set up the backend

```bash
cd backend
cp .env.example .env        # fill in your API keys and database URL
pip install -e ".[dev]"
alembic upgrade head        # run database migrations
uvicorn app.main:app --reload --port 8000
```

The API will be running at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive API documentation.

### 3. Set up the frontend

```bash
cd frontend
cp .env.example .env.local  # set NEXT_PUBLIC_API_URL=http://localhost:8000
npm install
npm run dev
```

The app will be running at `http://localhost:3000`.

---

## Environment Variables

All required environment variables are documented in:
- `backend/.env.example` — API keys, database URL, JWT secret, Claude settings
- `frontend/.env.example` — backend API URL

**Never commit a real `.env` file.** The `.gitignore` already excludes them.

---

## Contributing

This project is in early development. If you'd like to contribute:

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Open a PR against `develop` using the [PR template](.github/PULL_REQUEST_TEMPLATE.md)

Please follow the [Conventional Commits](https://www.conventionalcommits.org/) format for commit messages (e.g. `feat(frontend): add stock search autocomplete`).

---

## CI/CD

Every pull request automatically runs:

- **Frontend**: ESLint, TypeScript type check, Next.js build
- **Backend**: Ruff linting, type check (mypy), pytest test suite

Workflows only run for the package that changed — a frontend-only PR won't trigger backend CI and vice versa.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

*Built with Claude Code by Anthropic.*
