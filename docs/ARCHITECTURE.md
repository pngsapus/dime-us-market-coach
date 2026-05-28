# Architecture

## Backend

FastAPI exposes `/api/*` endpoints. Mock market data is isolated behind `MarketDataProvider` so real providers can be added later without rewriting rule logic.

## Provider Layer

Phase 2B prepares a provider registry while keeping mock/local as the only active provider.

- Provider interface: `app/services/providers/base.py`.
- Active mock provider: `app/services/providers/mock_provider.py`.
- Provider resolver: `app/services/providers/provider_registry.py`.
- Config key: `MARKET_DATA_PROVIDER`, defaulting to `mock`.
- Unknown provider names safely fall back to mock/local and are reported as degraded in `/api/data-status`.
- No API keys, real providers, Dime API, or external calls are used.

Provider methods:

- `get_market_summary()`
- `get_stock_universe()`
- `get_stock_snapshot(symbol)`
- `get_data_status()`

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

Provider registry -> mock/local provider -> deterministic engines -> API contracts -> Thai UI pages.

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
- Phase 2B moves local universe access behind the provider layer; discovery scores the active provider universe instead of owning raw data directly.

No AI decision-making is used in V1.
