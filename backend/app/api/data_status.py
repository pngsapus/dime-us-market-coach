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
        message="Mock provider และ local discovery engine พร้อมใช้งาน แต่ไม่ใช่ราคาจาก Dime โดยตรง",
        limitations=[
            "ข้อมูลตลาดยังเป็น mock/local data เท่านั้น",
            "Discovery engine เป็น rule-based local mock data และไม่เรียก external API",
            "ราคาจาก Dime ยังเป็น manual input โดยผู้ใช้เท่านั้น",
            "ยังไม่เชื่อมต่อ Dime API หรือ broker/trading integration",
            "ยังไม่มีการแจ้งเตือนแบบเรียลไทม์หรือ LINE Official Account",
        ],
    )
