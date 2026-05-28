from fastapi import APIRouter

from app.schemas.contracts import DataStatus
from app.services.providers.mock_provider import provider

router = APIRouter(tags=["data-status"])


@router.get("/data-status", response_model=DataStatus)
def get_data_status() -> DataStatus:
    freshness = provider.get_market_summary().data_freshness
    return DataStatus(
        provider=freshness.provider,
        health="healthy" if not freshness.is_stale else "degraded",
        freshness=freshness,
        message="Mock provider พร้อมใช้งาน แต่ไม่ใช่ราคาจาก Dime โดยตรง",
        limitations=[
            "ยังไม่เชื่อมต่อข้อมูลตลาดจริง",
            "ยังไม่เชื่อมต่อ Dime API",
            "ยังไม่มีการแจ้งเตือนแบบเรียลไทม์",
        ],
    )
