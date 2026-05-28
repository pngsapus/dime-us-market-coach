# Architecture

## Backend

FastAPI exposes `/api/*` endpoints. Mock market data is isolated behind `MarketDataProvider` so real providers can be added later without rewriting rule logic.

Core deterministic services:

- `RuleEngine`: produces statuses from explicit input values.
- `RiskEngine`: calculates Risk:Reward, max position size, expected loss, and expected profit.
- `ExplanationEngine`: converts rule and plan results into beginner-friendly Thai with traceability.
- `LocalMarketDiscoveryEngine`: ranks a local/mock US stock and ETF universe using deterministic scoring rules.
- `DimeCostModel`: placeholder for future Dime fee/cost estimation.
- `NotificationCenter`: placeholder for future in-app, LINE OA, Telegram, and email notifications.

## Persistence

V1 uses SQLite for user-editable data while market data remains mock-only.

- Default database path: `backend/data/app.db`.
- The data directory is created automatically when the backend first reads or writes persisted data.
- Schema initialization is handled in `app/services/sqlite_store.py` with simple `CREATE TABLE IF NOT EXISTS` statements.
- No migration framework is used yet.
- `GET /api/settings/risk-profile` returns the saved risk profile, or the default profile if no row exists.
- `POST /api/settings/risk-profile` upserts the single saved risk profile.
- `GET /api/journal` returns persisted journal entries newest first.
- `POST /api/journal` validates and inserts a persisted journal entry.
- Tests can override the database path with `DIME_DB_PATH`.

## Frontend

Next.js App Router pages mirror the V1 workflow:

- `/dashboard`
- `/radar`
- `/stocks/[symbol]/explain`
- `/stocks/[symbol]/practice-plan`
- `/dime-check`
- `/journal`
- `/settings`
- `/data-status`

## Data Flow

Mock provider -> deterministic engines -> API contracts -> Thai UI pages.

Settings and Journal use SQLite persistence behind stable API contracts.

## Local Discovery

Phase 2A adds a local discovery layer for Radar without external market data.

- The local universe contains NVDA, AMD, MSFT, AAPL, TSLA, QQQ, COST, AMZN, GOOGL, and META.
- Discovery scoring is deterministic and uses local fields such as trend, momentum, quality, valuation risk, volatility risk, liquidity, and beginner fit.
- `GET /api/discovery/latest` returns the latest ranked output, creating a local mock run if no output exists yet.
- `POST /api/discovery/run` runs the local scoring engine and writes `backend/data/discovery/latest_discovery.json`.
- Timestamped snapshots are written under `backend/data/discovery/history/`.
- Runtime JSON outputs are ignored by git; `.gitkeep` files preserve the folders.
- `/api/radar` remains compatible by returning `StockSnapshot[]`, ordered from the latest discovery ranking.

No AI decision-making is used in V1.
