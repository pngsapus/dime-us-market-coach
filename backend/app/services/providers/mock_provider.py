from datetime import datetime, timezone

from fastapi import HTTPException

from app.schemas.contracts import DataFreshness, MarketSummary, StockSnapshot
from app.services.discovery_engine import discovery_engine


def _fresh(age_minutes: int = 12, stale: bool = False) -> DataFreshness:
    return DataFreshness(
        provider="mock_provider",
        source="mock market snapshot",
        as_of=datetime.now(timezone.utc),
        age_minutes=age_minutes,
        is_stale=stale,
        note="ข้อมูลนี้ไม่ใช่ราคาจาก Dime โดยตรง",
    )


class MockMarketDataProvider:
    def __init__(self) -> None:
        self.discovery = discovery_engine

    def get_market_summary(self) -> MarketSummary:
        return MarketSummary(
            headline="ตลาดสหรัฐอยู่ในโหมดคัดเลือกหุ้นรายตัว",
            tone="ระมัดระวังแต่ยังมีธีมให้ติดตาม",
            status="ควรติดตามแบบคัดเลือก",
            summary_th=(
                "ภาพรวมจำลองวันนี้สะท้อนว่าหุ้นกลุ่มเทคโนโลยีขนาดใหญ่ยังเป็นจุดสนใจ "
                "แต่ผู้เริ่มต้นควรให้ความสำคัญกับโซนราคาและขนาดความเสี่ยงก่อนตัดสินใจเอง"
            ),
            indices={"S&P 500": 5320.0, "Nasdaq 100": 18840.0, "Dow Jones": 39210.0},
            cautions=[
                "ข้อมูลเป็น mock data ไม่ใช่ราคาจาก Dime โดยตรง",
                "ระบบไม่ส่งคำสั่งซื้อขายและไม่ทำนายราคาหุ้นอนาคต",
            ],
            data_freshness=_fresh(),
            explanation_trace=[
                "ใช้ mock index snapshot",
                "ตรวจสอบ provider freshness",
                "สรุปเป็น market context สำหรับผู้เริ่มต้น",
            ],
        )

    def list_stocks(self) -> list[StockSnapshot]:
        return [self.discovery.to_stock_snapshot(item) for item in self.discovery.universe()]

    def get_stock(self, symbol: str) -> StockSnapshot:
        item = self.discovery.get_universe_item(symbol)
        if not item:
            raise HTTPException(status_code=404, detail=f"Symbol {symbol.upper()} is not available in mock data")
        return self.discovery.to_stock_snapshot(item)


provider = MockMarketDataProvider()
