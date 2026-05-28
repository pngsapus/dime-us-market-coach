# API Contract

Base URL: `/api`

## Endpoints

- `GET /market/summary`
- `GET /radar`
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
