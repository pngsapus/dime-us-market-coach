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

- Dashboard: open `/dashboard`; confirm market summary, Radar preview, and `ข้อมูลนี้ไม่ใช่ราคาจาก Dime โดยตรง` are visible.
- Radar: open `/radar`; confirm NVDA, AMD, and TSLA render with score, status, reasons, cautions, and freshness.
- Stock Explain: open `/stocks/NVDA/explain`; confirm it is not blank and shows symbol, company name, status, price, VWAP, support, resistance, reasons, cautions, explanation trace, data freshness, Radar button, and Practice Plan button.
- Practice Plan: open `/stocks/NVDA/practice-plan`; confirm it shows backend mock plan data and does not show `frontend fallback`.
- Dime Check: open `/dime-check`; enter `134` for NVDA and confirm status `ไม่ควรไล่ซื้อ`.
- Dime Check: enter `131` for NVDA and confirm status `แผนยังอยู่ในเกณฑ์`.
- Dime Check: enter `128` for NVDA and confirm status `ราคายังไม่เข้าโซน`.
- Journal: open `/journal`; confirm Thai placeholders `เหตุผล` and `บทเรียนที่ได้`.
- Journal: save a valid entry and confirm `บันทึกเรียบร้อย` appears.
- Journal: confirm the new item appears in `รายการล่าสุด` without manually refreshing.
- Journal: submit with empty Symbol and confirm a Thai validation message appears.
- Journal: submit with empty reason and empty lesson learned and confirm a Thai validation message appears.
- Settings: open `/settings`; confirm Thai labels for risk profile fields.
- Settings: change risk values, click `บันทึก Risk Profile`, and confirm `บันทึก Risk Profile เรียบร้อย` appears.
- Settings: navigate away and back to `/settings`; confirm saved values remain visible during the same backend session.
- Data Status: open `/data-status`; confirm polished Thai provider and health labels.

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
- `GET /api/stocks/NVDA/explain`: `status`, `data_freshness`, `explanation_trace`, `reasons`, `cautions`
- `GET /api/stocks/NVDA/practice-plan`: `status`, `data_freshness`, `explanation_trace`, `reasons`, `cautions`
- `POST /api/dime/check-price`: `status`, `data_freshness`, `explanation_trace`, `reason`, `action`
- `GET /api/data-status`: provider health, freshness, and limitations
