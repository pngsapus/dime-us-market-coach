from datetime import datetime, timezone

from fastapi import HTTPException

from app.core.constants import STATUS_WAIT
from app.schemas.contracts import DataFreshness, LocalStockUniverseItem, MarketSummary, ProviderStatus, StockSnapshot
from app.services.providers.base import MarketDataProvider


def _fresh(age_minutes: int = 12, stale: bool = False, source: str = "mock market snapshot") -> DataFreshness:
    return DataFreshness(
        provider="mock",
        source=source,
        as_of=datetime.now(timezone.utc),
        age_minutes=age_minutes,
        is_stale=stale,
        note="ข้อมูลจำลองในเครื่อง ไม่ใช่ราคาจาก Dime โดยตรง",
    )


class MockMarketDataProvider(MarketDataProvider):
    provider_name = "mock"
    provider_type = "mock/local"

    def get_market_summary(self) -> MarketSummary:
        freshness = _fresh()
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
                "ข้อมูลเป็น mock/local data ไม่ใช่ราคาจาก Dime โดยตรง",
                "ระบบไม่ส่งคำสั่งซื้อขายและไม่ทำนายราคาหุ้นอนาคต",
            ],
            data_freshness=freshness,
            explanation_trace=[
                "ใช้ provider mock/local เป็นแหล่งข้อมูล",
                "ตรวจสอบ freshness ของข้อมูลจำลอง",
                "สรุปเป็น market context สำหรับผู้เริ่มต้น",
            ],
        )

    def get_stock_universe(self) -> list[LocalStockUniverseItem]:
        freshness = _fresh(age_minutes=15, source="local mock universe")
        stale_freshness = _fresh(age_minutes=95, stale=True, source="local mock universe")
        return [
            LocalStockUniverseItem(
                symbol="NVDA",
                name="NVIDIA Corporation",
                sector_theme="AI semiconductors",
                mock_price=132.4,
                mock_daily_change_pct=1.8,
                trend_score=88,
                momentum_score=84,
                quality_score=86,
                valuation_risk_score=72,
                volatility_risk_score=68,
                liquidity_score=95,
                beginner_fit_score=62,
                beginner_description="ผู้นำชิป AI ที่มีสภาพคล่องสูง แต่ราคาผันผวนและ valuation ต้องระวัง",
                data_status="mock_local",
                vwap=129.8,
                support=126.5,
                resistance=138.0,
                relative_volume=1.8,
                data_freshness=freshness,
            ),
            LocalStockUniverseItem(
                symbol="AMD",
                name="Advanced Micro Devices, Inc.",
                sector_theme="AI semiconductors",
                mock_price=164.2,
                mock_daily_change_pct=0.6,
                trend_score=66,
                momentum_score=58,
                quality_score=72,
                valuation_risk_score=65,
                volatility_risk_score=70,
                liquidity_score=88,
                beginner_fit_score=58,
                beginner_description="หุ้นชิปที่เกี่ยวข้องกับธีม AI แต่แรงยืนยันจำลองยังไม่เด่น",
                data_status="mock_local",
                vwap=165.1,
                support=158.0,
                resistance=172.0,
                relative_volume=1.2,
                data_freshness=freshness,
            ),
            LocalStockUniverseItem(
                symbol="MSFT",
                name="Microsoft Corporation",
                sector_theme="Cloud and AI software",
                mock_price=426.8,
                mock_daily_change_pct=0.4,
                trend_score=82,
                momentum_score=68,
                quality_score=92,
                valuation_risk_score=48,
                volatility_risk_score=38,
                liquidity_score=94,
                beginner_fit_score=84,
                beginner_description="ธุรกิจขนาดใหญ่ กระแสเงินสดแข็งแรง และผันผวนน้อยกว่าหุ้นธีมร้อนหลายตัว",
                data_status="mock_local",
                vwap=423.5,
                support=415.0,
                resistance=438.0,
                relative_volume=1.3,
                data_freshness=freshness,
            ),
            LocalStockUniverseItem(
                symbol="AAPL",
                name="Apple Inc.",
                sector_theme="Consumer technology",
                mock_price=191.3,
                mock_daily_change_pct=-0.2,
                trend_score=63,
                momentum_score=52,
                quality_score=88,
                valuation_risk_score=44,
                volatility_risk_score=34,
                liquidity_score=96,
                beginner_fit_score=82,
                beginner_description="หุ้นเทคโนโลยีขนาดใหญ่ที่เหมาะกับการฝึกดูโซนราคาและความเสี่ยงอย่างเป็นระบบ",
                data_status="mock_local",
                vwap=192.1,
                support=187.0,
                resistance=198.0,
                relative_volume=1.0,
                data_freshness=freshness,
            ),
            LocalStockUniverseItem(
                symbol="TSLA",
                name="Tesla, Inc.",
                sector_theme="EV and autonomy",
                mock_price=178.6,
                mock_daily_change_pct=-1.4,
                trend_score=48,
                momentum_score=42,
                quality_score=62,
                valuation_risk_score=78,
                volatility_risk_score=88,
                liquidity_score=92,
                beginner_fit_score=35,
                beginner_description="หุ้นที่มีสภาพคล่องสูงแต่ความผันผวนและ sentiment เปลี่ยนเร็ว จึงต้องระวังเป็นพิเศษ",
                data_status="mock_local_stale",
                vwap=181.3,
                support=172.0,
                resistance=190.0,
                relative_volume=0.9,
                data_freshness=stale_freshness,
            ),
            LocalStockUniverseItem(
                symbol="QQQ",
                name="Invesco QQQ Trust",
                sector_theme="Nasdaq 100 ETF",
                mock_price=462.1,
                mock_daily_change_pct=0.5,
                trend_score=78,
                momentum_score=67,
                quality_score=80,
                valuation_risk_score=42,
                volatility_risk_score=45,
                liquidity_score=98,
                beginner_fit_score=88,
                beginner_description="ETF ที่ใช้ฝึกมองภาพรวม Nasdaq 100 ได้ง่ายกว่าหุ้นรายตัวบางตัว",
                data_status="mock_local",
                vwap=459.6,
                support=452.0,
                resistance=470.0,
                relative_volume=1.2,
                data_freshness=freshness,
            ),
            LocalStockUniverseItem(
                symbol="COST",
                name="Costco Wholesale Corporation",
                sector_theme="Defensive consumer retail",
                mock_price=817.4,
                mock_daily_change_pct=0.3,
                trend_score=76,
                momentum_score=61,
                quality_score=90,
                valuation_risk_score=62,
                volatility_risk_score=32,
                liquidity_score=74,
                beginner_fit_score=76,
                beginner_description="ธุรกิจค้าปลีกคุณภาพสูง เหมาะกับการฝึกเทียบคุณภาพกับ valuation risk",
                data_status="mock_local",
                vwap=812.0,
                support=798.0,
                resistance=832.0,
                relative_volume=1.1,
                data_freshness=freshness,
            ),
            LocalStockUniverseItem(
                symbol="AMZN",
                name="Amazon.com, Inc.",
                sector_theme="Cloud and ecommerce",
                mock_price=184.7,
                mock_daily_change_pct=0.9,
                trend_score=80,
                momentum_score=72,
                quality_score=82,
                valuation_risk_score=54,
                volatility_risk_score=52,
                liquidity_score=94,
                beginner_fit_score=72,
                beginner_description="มีทั้งธุรกิจ cloud และ ecommerce จึงเหมาะกับการฝึกแยกธีมและปัจจัยเสี่ยง",
                data_status="mock_local",
                vwap=181.9,
                support=176.0,
                resistance=191.0,
                relative_volume=1.5,
                data_freshness=freshness,
            ),
            LocalStockUniverseItem(
                symbol="GOOGL",
                name="Alphabet Inc.",
                sector_theme="Search, ads, and AI",
                mock_price=173.2,
                mock_daily_change_pct=0.2,
                trend_score=73,
                momentum_score=60,
                quality_score=87,
                valuation_risk_score=40,
                volatility_risk_score=41,
                liquidity_score=91,
                beginner_fit_score=80,
                beginner_description="หุ้น mega-cap ที่ใช้ฝึกดูคุณภาพธุรกิจและความเสี่ยงด้าน regulation ได้",
                data_status="mock_local",
                vwap=172.5,
                support=168.0,
                resistance=179.0,
                relative_volume=1.1,
                data_freshness=freshness,
            ),
            LocalStockUniverseItem(
                symbol="META",
                name="Meta Platforms, Inc.",
                sector_theme="Social platforms and AI ads",
                mock_price=512.6,
                mock_daily_change_pct=1.1,
                trend_score=84,
                momentum_score=76,
                quality_score=84,
                valuation_risk_score=58,
                volatility_risk_score=56,
                liquidity_score=90,
                beginner_fit_score=70,
                beginner_description="แรงกำไรและธีม AI ads น่าสนใจ แต่ราคายังผันผวนตาม sentiment ของกลุ่มเทค",
                data_status="mock_local",
                vwap=506.3,
                support=492.0,
                resistance=528.0,
                relative_volume=1.4,
                data_freshness=freshness,
            ),
        ]

    def get_stock_snapshot(self, symbol: str) -> StockSnapshot:
        item = self._get_universe_item(symbol)
        return StockSnapshot(
            symbol=item.symbol,
            company_name=item.name,
            price=item.mock_price,
            vwap=item.vwap,
            support=item.support,
            resistance=item.resistance,
            relative_volume=item.relative_volume,
            market_context=f"{item.sector_theme}: {item.beginner_description}",
            score=item.trend_score,
            status=STATUS_WAIT,
            reasons=[
                "ข้อมูลมาจาก provider mock/local",
                "ใช้สำหรับเตรียมโครงสร้างข้อมูลก่อนเชื่อมต่อผู้ให้บริการจริง",
            ],
            cautions=[
                "ข้อมูลนี้ไม่ใช่ราคาจาก Dime โดยตรง",
                "ยังไม่มีการเชื่อมต่อข้อมูลตลาดจริง",
            ],
            explanation_trace=[
                f"อ่าน {item.symbol} จาก mock provider",
                "แปลง local universe item เป็น StockSnapshot",
                "ยังไม่มี external API หรือ Dime API ในขั้นนี้",
            ],
            data_freshness=item.data_freshness,
        )

    def get_data_status(self) -> ProviderStatus:
        now = datetime.now(timezone.utc)
        return ProviderStatus(
            provider_name=self.provider_name,
            provider_type=self.provider_type,
            is_available=True,
            is_live_data=False,
            is_direct_dime_data=False,
            last_updated=now,
            freshness_label="ข้อมูลจำลองในเครื่องพร้อมใช้งาน",
            limitations=[
                "ยังไม่เชื่อมต่อข้อมูลตลาดจริง",
                "ยังไม่เชื่อมต่อ Dime API",
                "ยังไม่มี broker/trading integration",
            ],
            disclaimer="ข้อมูลจาก provider mock/local ใช้เพื่อการวิเคราะห์และฝึกวางแผนเท่านั้น ไม่ใช่ราคาจาก Dime โดยตรง",
        )

    def _get_universe_item(self, symbol: str) -> LocalStockUniverseItem:
        normalized = symbol.upper()
        for item in self.get_stock_universe():
            if item.symbol == normalized:
                return item
        raise HTTPException(status_code=404, detail=f"Symbol {normalized} is not available in mock provider")


provider = MockMarketDataProvider()
