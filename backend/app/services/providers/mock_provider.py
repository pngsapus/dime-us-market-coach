from datetime import datetime, timezone

from fastapi import HTTPException

from app.core.constants import STATUS_FOLLOW, STATUS_WAIT
from app.schemas.contracts import DataFreshness, MarketSummary, StockSnapshot


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
        self._stocks = {
            "NVDA": StockSnapshot(
                symbol="NVDA",
                company_name="NVIDIA Corporation",
                price=132.4,
                vwap=129.8,
                support=126.5,
                resistance=138.0,
                relative_volume=1.8,
                market_context="กลุ่ม semiconductor ยังมีแรงติดตามจากธีม AI แต่ราคาผันผวนสูง",
                score=82,
                status=STATUS_FOLLOW,
                reasons=["ราคาอยู่เหนือ VWAP", "Relative Volume สูง", "ยังอยู่ใกล้โซนแผนมากกว่าการไล่ราคา"],
                cautions=["หุ้นผันผวนสูง", "หากราคาจริงใน Dime สูงกว่าโซนแผนควรรอจังหวะใหม่"],
                explanation_trace=[
                    "mock_provider โหลดข้อมูล NVDA",
                    "price 132.4 > vwap 129.8",
                    "relative_volume 1.8 >= 1.4",
                ],
                data_freshness=_fresh(),
            ),
            "AMD": StockSnapshot(
                symbol="AMD",
                company_name="Advanced Micro Devices, Inc.",
                price=164.2,
                vwap=165.1,
                support=158.0,
                resistance=172.0,
                relative_volume=1.2,
                market_context="ชิป AI ยังเป็นธีมหลัก แต่แรงยืนยันวันนี้ยังไม่เด่นเท่า NVDA",
                score=64,
                status=STATUS_WAIT,
                reasons=["ราคาใกล้ VWAP", "ยังไม่เห็นแรงปริมาณซื้อขายชัดเจน"],
                cautions=["ถ้าหลุดแนวรับ แผนจำลองควรถูกยกเลิก", "ควรรอข้อมูลยืนยันเพิ่ม"],
                explanation_trace=[
                    "mock_provider โหลดข้อมูล AMD",
                    "price 164.2 <= vwap 165.1",
                    "relative_volume 1.2 < 1.4",
                ],
                data_freshness=_fresh(),
            ),
            "TSLA": StockSnapshot(
                symbol="TSLA",
                company_name="Tesla, Inc.",
                price=178.6,
                vwap=181.3,
                support=172.0,
                resistance=190.0,
                relative_volume=0.9,
                market_context="หุ้นมีความผันผวนจากข่าวและ sentiment สูง จึงต้องเข้มงวดเรื่องความเสี่ยง",
                score=45,
                status=STATUS_WAIT,
                reasons=["ราคายังต่ำกว่า VWAP", "Relative Volume ยังไม่ยืนยัน"],
                cautions=["ข่าวเฉพาะบริษัทอาจทำให้ราคากระโดด", "ไม่ควรใช้แผนหากข้อมูล stale"],
                explanation_trace=[
                    "mock_provider โหลดข้อมูล TSLA",
                    "price 178.6 <= vwap 181.3",
                    "relative_volume 0.9 < 1.4",
                ],
                data_freshness=_fresh(92, True),
            ),
        }

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
        return list(self._stocks.values())

    def get_stock(self, symbol: str) -> StockSnapshot:
        stock = self._stocks.get(symbol.upper())
        if not stock:
            raise HTTPException(status_code=404, detail=f"Symbol {symbol.upper()} is not available in mock data")
        return stock


provider = MockMarketDataProvider()
