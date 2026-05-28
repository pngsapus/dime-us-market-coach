# Rule Engine

Rule decisions are deterministic and based on explicit inputs.

## Stock Status Rules

- If `data_freshness.is_stale` is true, status is `ข้อมูลไม่เพียงพอ`.
- If price is above VWAP and relative volume is at least `1.4`, status is `ควรติดตาม`.
- If price is at or below VWAP, status is `รอจังหวะ`.
- Otherwise status remains `รอจังหวะ` until confirmation is stronger.

## Dime Check Rules

- If provider data is stale, status is `ข้อมูลไม่เพียงพอ`.
- If user-entered Dime price is above the entry zone, status is `ไม่ควรไล่ซื้อ`.
- If user-entered Dime price is below the entry zone, status is `ราคายังไม่เข้าโซน`.
- If price is inside the entry zone but Risk:Reward is below profile minimum, status is `ไม่ควรไล่ซื้อ`.
- If price is inside the entry zone and Risk:Reward passes, status is `แผนยังอยู่ในเกณฑ์`.

## Phase 2A Local Discovery Scoring

Discovery scoring is deterministic and uses local/mock data only.

Phase 2B keeps the same scoring rules, but the discovery engine now reads the stock universe from the active provider layer instead of owning raw universe data directly. The active provider is still `mock`.

Phase 2C keeps scoring unchanged. If provider resolution falls back to mock/local, discovery still scores the fallback mock universe and `/api/data-status` reports the fallback/degraded provider state.

Weighted score:

- `trend_score` weight 22%.
- `momentum_score` weight 18%.
- `quality_score` weight 16%.
- `liquidity_score` weight 16%.
- `beginner_fit_score` weight 18%.
- `valuation_risk_score` subtracts 5%.
- `volatility_risk_score` subtracts 5%.

Category rules:

- If `data_freshness.is_stale` is true, category is `ข้อมูลไม่พอ`.
- If `volatility_risk_score >= 78` or `valuation_risk_score >= 82`, category is `ควรระวัง`.
- If final score is at least 70, category is `ควรติดตาม`.
- Otherwise category is `รอจังหวะ`.

Every discovery result must include `key_reasons`, `caution_points`, `explanation_trace`, `data_freshness`, and a disclaimer that the data is local/mock and not direct Dime realtime price.
