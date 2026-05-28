# Architecture

## Backend

FastAPI exposes `/api/*` endpoints. Mock market data is isolated behind `MarketDataProvider` so real providers can be added later without rewriting rule logic.

Core deterministic services:

- `RuleEngine`: produces statuses from explicit input values.
- `RiskEngine`: calculates Risk:Reward, max position size, expected loss, and expected profit.
- `ExplanationEngine`: converts rule and plan results into beginner-friendly Thai with traceability.
- `DimeCostModel`: placeholder for future Dime fee/cost estimation.
- `NotificationCenter`: placeholder for future in-app, LINE OA, Telegram, and email notifications.

## Frontend

Next.js App Router pages mirror the V1 workflow:

- `/dashboard`
- `/radar`
- `/stocks/[symbol]/explain`
- `/stocks/[symbol]/practice-plan`
- `/dime-check`
- `/journal`
- `/settings`
- `/data-status`

## Data Flow

Mock provider -> deterministic engines -> API contracts -> Thai UI pages.

No AI decision-making is used in V1.
