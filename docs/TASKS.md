# Tasks

## Completed

- Created backend FastAPI project structure.
- Added mock provider for NVDA, AMD, and TSLA.
- Added deterministic Rule Engine, Risk Engine, and Explanation Engine.
- Added Dime cost model and notification placeholders.
- Added V1 API endpoints.
- Added backend tests for risk, Dime Check, rule status, stale data, and explanation trace.
- Created Next.js frontend structure and eight V1 pages.
- Added persistent docs and `AGENTS.md`.
- Phase 1A: fixed Stock Explain routing for newer Next.js dynamic params.
- Phase 1A: removed silent frontend fallback data for market, radar, stock explain, practice plan, and data status.
- Phase 1A: improved Dime Check result card and below-zone status.
- Phase 1A: polished Thai UI labels for freshness, journal, settings, data status, and plan flow.
- Phase 1A: added manual QA checklist.
- Fixed Settings and Journal save flows so both submit to backend mock API, show success/error banners, and preserve in-memory results during the backend session.
- Added backend tests for saving Risk Profile and Journal entries.
- Added backend Journal validation for missing symbol, decision, and missing reason/lesson.
- Fixed Settings submit button stuck state by replacing click-based pending state with form submission status and adding timeout handling for backend calls.
- Phase 1B: replaced in-memory Settings and Journal storage with SQLite persistence.
- Phase 1B: added automatic SQLite schema initialization under `backend/data/app.db`.
- Phase 1B: added backend tests for repository reload persistence and newest-first Journal ordering.
- Phase 1C: added reusable frontend UI primitives for page headers, cards, data freshness, explanation traces, warnings, empty/error states, and success banners.
- Phase 1C: tightened the main user flow from Dashboard to Radar, Stock Explain, Practice Plan, Dime Check, and Journal.
- Phase 1C: polished Thai copy and clarified mock/degraded data boundaries across key pages.
- Phase 1C: added app-level loading and error states to avoid blank pages.
- Phase 1D: completed QA stabilization pass across key pages, API smoke checks, responsive layout checks, persistence restart checks, and forbidden wording scan.
- Phase 1D: fixed small Thai copy/documentation inconsistencies found during QA, including remaining English page wording and below-zone Dime Check documentation.
- Phase 2A: added a local rule-based market discovery engine with a 10-symbol mock US stock/ETF universe.
- Phase 2A: added `GET /api/discovery/latest` and `POST /api/discovery/run`.
- Phase 2A: updated Radar to show ranked discovery output with scoring categories, reasons, cautions, traces, and mock data warnings.
- Phase 2A: updated Dashboard to preview the top 3 discovery items and latest discovery run time.
- Phase 2A: expanded Stock Explain and Practice Plan compatibility for new local universe symbols.
- Phase 2A: added discovery output folders under `backend/data/discovery/` with runtime JSON ignored by git.
- Phase 2A: added backend tests for discovery scoring, endpoints, and Radar compatibility.
- Phase 2A.1: cleaned up Radar UX copy, clarified sidebar vs recommended next steps, simplified cards, and translated discovery traces/categories for beginners.
- Phase 2B: added backend market data provider abstraction and provider registry.
- Phase 2B: kept `MARKET_DATA_PROVIDER=mock` as the default and added unknown-provider fallback to mock/local.
- Phase 2B: moved the local stock universe behind the mock provider so discovery consumes provider data.
- Phase 2B: expanded `/api/data-status` with provider readiness, live-data, Dime-source, trading-integration, and discovery-mode fields.
- Phase 2B: added backend tests for provider registry, fallback behavior, mock provider output, provider-based discovery, and data status.

## Next

- Add frontend component tests or Playwright smoke tests.
- Add real provider interface implementation only after explicit approval.
