from fastapi import APIRouter

from app.schemas.contracts import MarketSummary
from app.services.providers.provider_registry import get_active_provider

router = APIRouter(tags=["market"])


@router.get("/market/summary", response_model=MarketSummary)
def get_market_summary() -> MarketSummary:
    return get_active_provider().get_market_summary()
