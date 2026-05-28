# Decisions

## 2026-05-28

- Use FastAPI for backend and Next.js App Router for frontend.
- Use mock provider only in V1.
- Keep Rule Engine, Risk Engine, and Explanation Engine deterministic.
- Use in-memory journal/settings for scaffold speed; SQLite remains the V1 persistence target for the next implementation phase.
- Dime Check accepts user-entered price and does not claim direct Dime realtime data.
- Notification Center is an in-app placeholder only.

## 2026-05-28 Phase 1B

- Replace in-memory Settings and Journal storage with SQLite for V1 persistence.
- Store the default database at `backend/data/app.db`.
- Create the `backend/data` directory automatically if missing.
- Keep API contracts stable for `GET/POST /api/settings/risk-profile` and `GET/POST /api/journal`.
- Avoid migration tooling for now; use simple schema initialization in the backend repository layer.

## 2026-05-28 Phase 2A

- Add a local rule-based discovery engine before connecting any real market data provider.
- Store generated discovery runtime JSON under `backend/data/discovery/` and keep those JSON files out of git.
- Keep `/api/radar` compatible while adding richer discovery endpoints for the Radar UI.
- Expand the local mock universe to 10 US stocks/ETFs so Stock Explain and Practice Plan can support Radar symbols beyond NVDA, AMD, and TSLA.
