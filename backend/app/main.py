from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import data_status, dime, journal, market, notifications, radar, settings, stocks

app = FastAPI(
    title="Dime US Market Coach",
    description="Beginner-friendly US stock analysis assistant using mock data only.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market.router, prefix="/api")
app.include_router(radar.router, prefix="/api")
app.include_router(stocks.router, prefix="/api")
app.include_router(dime.router, prefix="/api")
app.include_router(journal.router, prefix="/api")
app.include_router(settings.router, prefix="/api")
app.include_router(data_status.router, prefix="/api")
app.include_router(notifications.router, prefix="/api")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "mode": "mock"}
