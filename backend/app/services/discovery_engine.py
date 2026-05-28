from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from pydantic import ValidationError

from app.core.constants import STATUS_FOLLOW, STATUS_WAIT
from app.schemas.contracts import DataFreshness, DiscoveryResult, DiscoveryRun, LocalStockUniverseItem, StockSnapshot

DISCOVERY_DISCLAIMER = "ข้อมูล Radar เป็นข้อมูลจำลองในเครื่อง ไม่ใช่ราคาจาก Dime โดยตรง และไม่ใช่คำสั่งซื้อ"
STATUS_HIGH_RISK_CAUTION = "ควรระวัง"
STATUS_DISCOVERY_INSUFFICIENT = "ข้อมูลไม่พอ"


def _freshness(age_minutes: int = 15, stale: bool = False) -> DataFreshness:
    return DataFreshness(
        provider="local_discovery_mock",
        source="local mock universe",
        as_of=datetime.now(timezone.utc),
        age_minutes=age_minutes,
        is_stale=stale,
        note="ข้อมูลจำลองในเครื่อง ไม่ใช่ราคาจาก Dime โดยตรง",
    )


def _project_backend_dir() -> Path:
    return Path(__file__).resolve().parents[2]


class LocalMarketDiscoveryEngine:
    def __init__(self, output_dir: Path | None = None) -> None:
        self.output_dir = output_dir or (_project_backend_dir() / "data" / "discovery")
        self.history_dir = self.output_dir / "history"

    def universe(self) -> list[LocalStockUniverseItem]:
        freshness = _freshness()
        stale_freshness = _freshness(age_minutes=95, stale=True)
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

    def score_item(self, item: LocalStockUniverseItem) -> DiscoveryResult:
        raw_score = (
            item.trend_score * 0.22
            + item.momentum_score * 0.18
            + item.quality_score * 0.16
            + item.liquidity_score * 0.16
            + item.beginner_fit_score * 0.18
            - item.valuation_risk_score * 0.05
            - item.volatility_risk_score * 0.05
        )
        final_score = max(0, min(100, round(raw_score)))

        if item.data_freshness.is_stale:
            category = STATUS_DISCOVERY_INSUFFICIENT
        elif item.volatility_risk_score >= 78 or item.valuation_risk_score >= 82:
            category = STATUS_HIGH_RISK_CAUTION
        elif final_score >= 70:
            category = STATUS_FOLLOW
        else:
            category = STATUS_WAIT

        reasons = [
            f"แนวโน้ม {item.trend_score}/100 และโมเมนตัม {item.momentum_score}/100",
            f"คุณภาพ {item.quality_score}/100 และสภาพคล่อง {item.liquidity_score}/100",
            f"ความเหมาะสมกับมือใหม่ {item.beginner_fit_score}/100 จากความง่ายในการติดตามธีมและความเสี่ยง",
        ]
        cautions = [
            f"ความเสี่ยงด้านมูลค่า {item.valuation_risk_score}/100",
            f"ความเสี่ยงด้านความผันผวน {item.volatility_risk_score}/100",
            "ต้องตรวจสอบราคาจริงใน Dime ด้วยตนเองก่อนใช้ประกอบการพิจารณา",
        ]
        if item.data_freshness.is_stale:
            cautions.insert(0, "ข้อมูลจำลองชุดนี้ล่าช้า จึงไม่ควรสรุปเชิงมั่นใจ")
        elif category == STATUS_HIGH_RISK_CAUTION:
            cautions.insert(0, "คะแนนรวมมีบางด้านน่าสนใจ แต่ความเสี่ยงสูงกว่าที่เหมาะกับผู้เริ่มต้นบางคน")

        trace = [
            "ระบบเริ่มจากรายการหุ้นจำลองในเครื่อง",
            "คำนวณคะแนนจากแนวโน้ม โมเมนตัม คุณภาพ สภาพคล่อง และความเหมาะสมกับมือใหม่",
            "หักคะแนนจากความเสี่ยงด้านมูลค่าและความผันผวน",
            f"คะแนนรวมของ {item.symbol} คือ {final_score}/100",
            f"สรุปสถานะเป็น {category} เพื่อช่วยเลือกว่าจะศึกษาต่อหรือควรรอก่อน",
        ]

        return DiscoveryResult(
            symbol=item.symbol,
            name=item.name,
            sector_theme=item.sector_theme,
            beginner_summary=item.beginner_description,
            rank=0,
            final_score=final_score,
            category=category,
            key_reasons=reasons,
            caution_points=cautions,
            explanation_trace=trace,
            data_freshness=item.data_freshness,
            disclaimer=DISCOVERY_DISCLAIMER,
            mock_price=item.mock_price,
            mock_daily_change_pct=item.mock_daily_change_pct,
            trend_score=item.trend_score,
            momentum_score=item.momentum_score,
            quality_score=item.quality_score,
            valuation_risk_score=item.valuation_risk_score,
            volatility_risk_score=item.volatility_risk_score,
            liquidity_score=item.liquidity_score,
            beginner_fit_score=item.beginner_fit_score,
        )

    def run(self, write_files: bool = True) -> DiscoveryRun:
        scored = [self.score_item(item) for item in self.universe()]
        scored.sort(key=lambda item: item.final_score, reverse=True)
        ranked = [item.model_copy(update={"rank": index + 1}) for index, item in enumerate(scored)]
        generated_at = datetime.now(timezone.utc)
        result = DiscoveryRun(
            generated_at=generated_at,
            universe_count=len(ranked),
            data_freshness=_freshness(),
            disclaimer=DISCOVERY_DISCLAIMER,
            results=ranked,
        )
        if write_files:
            self.write_output(result)
        return result

    def latest(self) -> DiscoveryRun:
        latest_path = self.output_dir / "latest_discovery.json"
        if not latest_path.exists():
            return self.run(write_files=True)
        try:
            return DiscoveryRun.model_validate_json(latest_path.read_text(encoding="utf-8"))
        except (ValidationError, json.JSONDecodeError):
            return self.run(write_files=True)

    def write_output(self, result: DiscoveryRun) -> None:
        self.history_dir.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2)
        (self.output_dir / "latest_discovery.json").write_text(payload + "\n", encoding="utf-8")
        stamp = result.generated_at.strftime("%Y%m%dT%H%M%SZ")
        (self.history_dir / f"{stamp}.json").write_text(payload + "\n", encoding="utf-8")

    def get_universe_item(self, symbol: str) -> LocalStockUniverseItem | None:
        normalized = symbol.upper()
        for item in self.universe():
            if item.symbol == normalized:
                return item
        return None

    def to_stock_snapshot(self, item: LocalStockUniverseItem) -> StockSnapshot:
        result = self.score_item(item)
        return StockSnapshot(
            symbol=item.symbol,
            company_name=item.name,
            price=item.mock_price,
            vwap=item.vwap,
            support=item.support,
            resistance=item.resistance,
            relative_volume=item.relative_volume,
            market_context=f"{item.sector_theme}: {item.beginner_description}",
            score=result.final_score,
            status=result.category,
            reasons=result.key_reasons,
            cautions=result.caution_points,
            explanation_trace=result.explanation_trace,
            data_freshness=item.data_freshness,
        )


discovery_engine = LocalMarketDiscoveryEngine()
