from fastapi import APIRouter

from app.schemas.contracts import MarketSummary
from app.services.providers.mock_provider import provider

router = APIRouter(tags=["market"])


@router.get("/market/summary", response_model=MarketSummary)
def get_market_summary() -> MarketSummary:
    return provider.get_market_summary()
