from fastapi import APIRouter

from app.schemas.contracts import DataStatus
from app.services.providers.provider_registry import get_active_provider, get_provider_resolution

router = APIRouter(tags=["data-status"])


@router.get("/data-status", response_model=DataStatus)
def get_data_status() -> DataStatus:
    provider = get_active_provider()
    resolution = get_provider_resolution()
    provider_status = provider.get_data_status()
    freshness = provider.get_market_summary().data_freshness
    health = "healthy" if provider_status.is_available and not resolution.used_fallback else "degraded"
    limitations = [
        "ข้อมูลตลาดยังเป็น mock/local data เท่านั้น",
        "Discovery engine เป็น local rule-based mock data และไม่เรียก external API",
        "ราคาจาก Dime ยังเป็น manual input โดยผู้ใช้เท่านั้น",
        "ยังไม่เชื่อมต่อ Dime API หรือ broker/trading integration",
        "ยังไม่มีการแจ้งเตือนแบบเรียลไทม์หรือ LINE Official Account",
    ]
    if resolution.used_fallback:
        limitations.insert(0, resolution.message)
    return DataStatus(
        provider=provider.provider_name,
        health=health,
        freshness=freshness,
        message=f"{resolution.message} ข้อมูลนี้ไม่ใช่ราคาจาก Dime โดยตรง",
        limitations=limitations,
        active_provider=provider.provider_name,
        provider_type=provider.provider_type,
        is_live_market_data_connected=provider_status.is_live_data,
        is_dime_price_source_connected=provider_status.is_direct_dime_data,
        has_trading_integration=False,
        is_discovery_local_rule_based=True,
        provider_status=provider_status,
    )
