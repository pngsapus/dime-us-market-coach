# API Contract

Base URL: `/api`

## Endpoints

- `GET /market/summary`
- `GET /radar`
- `GET /discovery/latest`
- `POST /discovery/run`
- `GET /stocks/{symbol}/explain`
- `GET /stocks/{symbol}/practice-plan`
- `POST /dime/check-price`
- `GET /journal`
- `POST /journal`
- `GET /settings/risk-profile`
- `POST /settings/risk-profile`
- `GET /data-status`
- `GET /notifications`

## Shared Requirements

- Analysis responses include `explanation_trace`.
- Market-related responses include `data_freshness`.
- Dime Check never assumes live Dime price; it only evaluates the user-entered price.
- Settings and Journal responses keep the same JSON shape while using SQLite persistence in V1.
- Discovery responses are local/mock only and must include `explanation_trace`, `data_freshness`, and a non-order disclaimer.
- Provider status responses must clearly show that mock/local is active, live data is not connected, Dime price source is manual input only, and no trading integration exists.

## Discovery Response

`GET /discovery/latest` and `POST /discovery/run` return:

```json
{
  "generated_at": "2026-05-28T00:00:00Z",
  "universe_count": 10,
  "data_freshness": {},
  "disclaimer": "ข้อมูล Radar เป็นข้อมูลจำลองในเครื่อง ไม่ใช่ราคาจาก Dime โดยตรง และไม่ใช่คำสั่งซื้อ",
  "results": [
    {
      "symbol": "MSFT",
      "name": "Microsoft Corporation",
      "sector_theme": "Cloud and AI software",
      "beginner_summary": "ธุรกิจขนาดใหญ่ กระแสเงินสดแข็งแรง และผันผวนน้อยกว่าหุ้นธีมร้อนหลายตัว",
      "rank": 1,
      "final_score": 75,
      "category": "ควรติดตาม",
      "key_reasons": [],
      "caution_points": [],
      "explanation_trace": [],
      "data_freshness": {},
      "mock_price": 426.8,
      "mock_daily_change_pct": 0.4,
      "trend_score": 82,
      "momentum_score": 68,
      "quality_score": 92,
      "valuation_risk_score": 48,
      "volatility_risk_score": 38,
      "liquidity_score": 94,
      "beginner_fit_score": 84
    }
  ]
}
```

`GET /radar` remains compatible with the existing `StockSnapshot[]` response shape, but the list is ordered by the latest local discovery ranking.

## Data Status Response

`GET /data-status` keeps existing fields and adds provider readiness details:

```json
{
  "provider": "mock",
  "health": "healthy",
  "message": "ใช้ mock/local provider ข้อมูลนี้ไม่ใช่ราคาจาก Dime โดยตรง",
  "active_provider": "mock",
  "provider_type": "mock/local",
  "is_live_market_data_connected": false,
  "is_dime_price_source_connected": false,
  "has_trading_integration": false,
  "is_discovery_local_rule_based": true,
  "provider_status": {
    "provider_available": true,
    "provider_name": "mock",
    "provider_type": "mock/local",
    "is_available": true,
    "is_live_data": false,
    "is_direct_dime_data": false,
    "is_degraded": false,
    "fallback_used": false,
    "fallback_reason": "",
    "freshness_label": "ข้อมูลจำลองในเครื่องพร้อมใช้งาน",
    "limitations": [],
    "disclaimer": "ข้อมูลจาก provider mock/local ใช้เพื่อการวิเคราะห์และฝึกวางแผนเท่านั้น ไม่ใช่ราคาจาก Dime โดยตรง"
  }
}
```

If `MARKET_DATA_PROVIDER` is unknown or points to the future stub, the active data source remains mock/local and `provider_status.fallback_used` is true with a beginner-readable `fallback_reason`.

## Dime Check Request

```json
{
  "symbol": "NVDA",
  "dime_price": 134.0
}
```

Optional overrides:

```json
{
  "entry_zone": { "low": 129.0, "high": 132.5 },
  "stop_loss": 125.5,
  "take_profit": 138.5
}
```
