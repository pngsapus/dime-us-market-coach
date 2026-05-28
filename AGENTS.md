# AGENTS.md

## Product Guardrails

- This is not an auto-trading app.
- Do not send, simulate sending, or prepare trading orders.
- Do not use direct buy/sell language such as `Buy Now`, `Strong Buy`, `ซื้อทันที`, `ซื้อเลย`, `เข้าซื้อเลย`, `กำไรแน่`, `หุ้นเด็ด`, or `สัญญาณเข้า`.
- Use analysis language such as `ควรติดตาม`, `รอจังหวะ`, `ไม่ควรไล่ซื้อ`, `แผนยังอยู่ในเกณฑ์`, and `แผนวิเคราะห์จำลอง`.
- Always show `data_freshness` for market, radar, stock, plan, and data-status outputs.
- Every analysis result must include `explanation_trace`.
- Rule Engine and Risk Engine must be deterministic and testable.
- Use mock data first unless explicitly asked to connect real market data.
- Do not connect Dime API unless explicitly requested in a future phase.
- Do not change the core architecture without updating `docs/DECISIONS.md`.

## Architecture

- Backend: Python, FastAPI, deterministic services.
- Frontend: Next.js, React, TypeScript, Tailwind CSS.
- V1 database target: SQLite, but current scaffold uses in-memory journal/settings for mock iteration.
- Contract-first API: update `docs/API_CONTRACT.md` when endpoint shapes change.
