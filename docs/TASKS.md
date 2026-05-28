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

## Next

- Add API integration tests for all endpoints.
- Add frontend component tests or Playwright smoke tests.
- Add real provider interface implementation only after explicit approval.
