# Manual QA Checklist

Use this checklist after starting backend and frontend locally.

Backend:

```powershell
cd C:\Dime\dime-us-market-coach\backend
python -m uvicorn app.main:app --reload
```

Frontend:

```powershell
cd C:\Dime\dime-us-market-coach\frontend
npm run dev
```

## Browser Checks

- Dashboard: open `/dashboard`; confirm market summary, Radar preview, warning box, freshness card, and `ข้อมูลนี้ไม่ใช่ราคาจาก Dime โดยตรง` are visible.
- Dashboard Radar preview: confirm top 3 items show rank, score, category, latest run time, and local/mock freshness.
- Dashboard flow: click `ไปที่ Radar`.
- Radar: confirm the local universe renders NVDA, AMD, MSFT, AAPL, TSLA, QQQ, COST, AMZN, GOOGL, and META.
- Radar: confirm the page explains that sidebar navigation can be used anytime and in-page buttons are recommended next steps only.
- Radar: confirm `วิธีใช้หน้านี้` explains status/score, reasons/cautions, choosing a stock, and going to explain/plan pages.
- Radar: confirm each item shows rank, symbol, company name, category/status badge, score, beginner summary, max 3 reasons, max 3 cautions, and short freshness label.
- Radar: expand `ดูรายละเอียดคะแนนและร่องรอยการจัดอันดับ` and confirm score components plus Thai explanation trace are visible.
- Radar flow: click `อ่านคำอธิบาย` for NVDA.
- Radar compatibility: click `อ่านคำอธิบาย` for a newer universe symbol such as MSFT and confirm Stock Explain works.
- Stock Explain: confirm it is not blank and shows symbol, company name, status, price, VWAP, support, resistance, reasons, cautions, explanation trace, data freshness, Radar button, and Practice Plan button.
- Stock Explain flow: click `ไปที่แผนวิเคราะห์จำลอง`.
- Practice Plan: confirm it shows backend mock plan data, warning box, explanation trace, and does not show `frontend fallback`.
- Practice Plan flow: click `ตรวจสอบราคาจริงใน Dime`.
- Dime Check: enter `134` for NVDA and confirm status `ไม่ควรไล่ซื้อ`, reason, Risk:Reward, action, disclaimer, and explanation trace.
- Dime Check: enter `131` for NVDA and confirm status `แผนยังอยู่ในเกณฑ์`.
- Dime Check: enter `128` for NVDA and confirm status `ราคายังไม่เข้าโซน`.
- Dime Check flow: click `บันทึกบทเรียนในบันทึกการฝึกวิเคราะห์`.
- Journal: open `/journal`; confirm Thai placeholders `เหตุผล` and `บทเรียนที่ได้`.
- Journal: save a valid entry and confirm `บันทึกเรียบร้อย` appears.
- Journal: confirm the new item appears in `รายการล่าสุด` without manually refreshing.
- Journal: submit with empty Symbol and confirm a Thai validation message appears.
- Journal: submit with empty reason and empty lesson learned and confirm a Thai validation message appears.
- Journal persistence: restart the backend and confirm saved entries are still visible.
- Settings: open `/settings`; confirm Thai labels for risk profile fields.
- Settings: change risk values, click `บันทึก Risk Profile`, and confirm `บันทึก Risk Profile เรียบร้อย` appears.
- Settings: navigate away and back to `/settings`; confirm saved values remain visible during the same backend session.
- Settings persistence: restart the backend and confirm saved values remain visible.
- Data Status: open `/data-status`; confirm polished Thai provider and health labels.
- Data Status: confirm it says market data is mock/local, Dime price source is manual input only, no external API is connected, no trading integration exists, and discovery is local rule-based mock data.
- Data Status provider layer: confirm active provider is mock/local, live market data is not connected, Dime price source is manual input only, trading integration is absent, and provider readiness says mock/local data is available.
- Data Status fallback fields: confirm mock fallback says it is not being used during normal `MARKET_DATA_PROVIDER=mock` startup.
- Provider QA: optionally start backend with `MARKET_DATA_PROVIDER=real_stub` or an unknown value and confirm `/api/data-status` reports fallback to mock/local without requiring credentials or external API calls.
- Loading/error states: stop backend temporarily and confirm affected pages show a visible error state instead of a blank page.
- Responsive layout: check `/dashboard`, `/radar`, `/stocks/NVDA/explain`, `/stocks/NVDA/practice-plan`, `/dime-check`, `/journal`, `/settings`, and `/data-status` on desktop and a narrow mobile viewport; confirm there is no horizontal overflow.
- Phase 1D restart check: save Settings and Journal through the frontend, restart only the backend, then confirm the saved Risk Profile and latest Journal entry remain visible.
- Phase 1D degraded-state check: stop the backend and reload `/dashboard`; confirm the page shows `ไม่สามารถเชื่อมต่อข้อมูลจำลองจาก backend ได้` with a retry action instead of stale analysis content.

## Forbidden Wording Check

Search app source and rendered pages for forbidden signal wording:

- `Buy Now`
- `Strong Buy`
- `ซื้อเลย`
- `เข้าทันที`
- `กำไรแน่`
- `หุ้นเด็ด`
- `สัญญาณเข้า`

The terms may appear only in guardrail documentation or constants that define forbidden copy, not in user-facing recommendations.

## Backend API Check

Confirm these endpoints return HTTP 200 and expected fields:

- `GET /api/market/summary`: `status`, `data_freshness`, `explanation_trace`, `cautions`
- `GET /api/radar`: each stock has `status`, `data_freshness`, `explanation_trace`, `reasons`, `cautions`
- `GET /api/discovery/latest`: ranked results with `rank`, `final_score`, `category`, `key_reasons`, `caution_points`, `explanation_trace`, `data_freshness`, and disclaimer
- `POST /api/discovery/run`: creates or updates local discovery output and returns the same ranked shape
- `GET /api/stocks/NVDA/explain`: `status`, `data_freshness`, `explanation_trace`, `reasons`, `cautions`
- `GET /api/stocks/MSFT/explain`: confirms Stock Explain supports new local universe symbols
- `GET /api/stocks/NVDA/practice-plan`: `status`, `data_freshness`, `explanation_trace`, `reasons`, `cautions`
- `POST /api/dime/check-price`: `status`, `data_freshness`, `explanation_trace`, `reason`, `action`
- `GET /api/data-status`: provider health, freshness, and limitations
- `GET /api/data-status`: provider readiness fields include `active_provider`, `provider_type`, `is_live_market_data_connected`, `is_dime_price_source_connected`, `has_trading_integration`, `is_discovery_local_rule_based`, and `provider_status`
- `GET /api/data-status`: `provider_status` includes `provider_available`, `is_degraded`, `fallback_used`, `fallback_reason`, `limitations`, `freshness_label`, and `disclaimer`

## Phase 1D QA Result

- Main flow rendered without blank pages during automated browser smoke checks.
- Dime Check returned `ไม่ควรไล่ซื้อ`, `แผนยังอยู่ในเกณฑ์`, and `ราคายังไม่เข้าโซน` for the tested price zones.
- Settings and Journal persisted after backend restart using `backend/data/app.db`.
- Desktop and 390px mobile checks showed no horizontal overflow across key pages.
- Forbidden wording scan across frontend/backend source returned no matches outside guardrail-only files.
