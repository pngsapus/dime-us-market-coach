from datetime import datetime, timezone

from fastapi import HTTPException

from app.schemas.contracts import DataFreshness, LocalStockUniverseItem, MarketSummary, ProviderStatus, StockSnapshot
from app.services.providers.base import MarketDataProvider


class RealMarketDataProviderStub(MarketDataProvider):
    provider_name = "real_stub"
    provider_type = "real-provider-stub"

    def get_market_summary(self) -> MarketSummary:
        freshness = self._freshness()
        return MarketSummary(
            headline="ยังไม่ได้เชื่อมต่อผู้ให้บริการข้อมูลตลาดจริง",
            tone="degraded",
            status="ข้อมูลไม่พอ",
            summary_th="โครงสร้าง provider จริงถูกเตรียมไว้เท่านั้น ยังไม่มีการเรียก external API และไม่มีข้อมูลตลาดจริง",
            indices={},
            cautions=[
                "ยังไม่ได้ตั้งค่า real market data provider",
                "ระบบ fallback ไปใช้ mock/local provider เมื่อใช้งานจริงใน registry",
            ],
            data_freshness=freshness,
            explanation_trace=[
                "เรียก real provider stub",
                "stub ไม่เชื่อมต่อ external API",
                "รายงานสถานะ not configured เท่านั้น",
            ],
        )

    def get_stock_universe(self) -> list[LocalStockUniverseItem]:
        return []

    def get_stock_snapshot(self, symbol: str) -> StockSnapshot:
        raise HTTPException(status_code=503, detail=f"Real provider stub is not configured for {symbol.upper()}")

    def get_data_status(self) -> ProviderStatus:
        return ProviderStatus(
            provider_available=False,
            provider_name=self.provider_name,
            provider_type=self.provider_type,
            is_available=False,
            is_live_data=False,
            is_direct_dime_data=False,
            is_degraded=True,
            fallback_used=False,
            fallback_reason="real provider stub ยังไม่ถูก implement และไม่มี credentials",
            last_updated=datetime.now(timezone.utc),
            freshness_label="ยังไม่พร้อมใช้งาน",
            limitations=[
                "stub นี้ไม่เรียก external API",
                "stub นี้ไม่ใช้ API key หรือ credentials",
                "ยังไม่มีข้อมูลตลาดจริง",
            ],
            disclaimer="Real provider stub มีไว้เตรียมโครงสร้างเท่านั้น ระบบยังใช้ mock/local data เป็นแหล่งข้อมูล active",
            degraded_reason="not configured / not implemented",
        )

    def _freshness(self) -> DataFreshness:
        return DataFreshness(
            provider=self.provider_name,
            source="real provider stub",
            as_of=datetime.now(timezone.utc),
            age_minutes=0,
            is_stale=True,
            note="ยังไม่ได้เชื่อมต่อข้อมูลตลาดจริง",
        )
