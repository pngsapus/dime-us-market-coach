# Dime US Market Coach Backend

FastAPI backend for the V1 mock-only analysis assistant.

## Run

```powershell
cd C:\Dime\dime-us-market-coach\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Test

```powershell
cd C:\Dime\dime-us-market-coach\backend
pytest
```

## Guardrails

- Mock data only.
- No Dime API connection.
- No trading orders.
- No direct buy/sell language.
- Every analysis result includes `explanation_trace` and `data_freshness`.
