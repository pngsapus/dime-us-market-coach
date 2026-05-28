# Decisions

## 2026-05-28

- Use FastAPI for backend and Next.js App Router for frontend.
- Use mock provider only in V1.
- Keep Rule Engine, Risk Engine, and Explanation Engine deterministic.
- Use in-memory journal/settings for scaffold speed; SQLite remains the V1 persistence target for the next implementation phase.
- Dime Check accepts user-entered price and does not claim direct Dime realtime data.
- Notification Center is an in-app placeholder only.
