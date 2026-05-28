from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from pydantic import ValidationError

from app.core.constants import STATUS_FOLLOW, STATUS_WAIT
from app.schemas.contracts import DataFreshness, DiscoveryResult, DiscoveryRun, LocalStockUniverseItem, StockSnapshot
from app.services.providers.base import MarketDataProvider

DISCOVERY_DISCLAIMER = "ข้อมูล Radar เป็นข้อมูลจำลองในเครื่อง ไม่ใช่ราคาจาก Dime โดยตรง และไม่ใช่คำสั่งซื้อ"
STATUS_HIGH_RISK_CAUTION = "ควรระวัง"
STATUS_DISCOVERY_INSUFFICIENT = "ข้อมูลไม่พอ"
SUPPORTED_DISCOVERY_CATEGORIES = {STATUS_FOLLOW, STATUS_WAIT, STATUS_HIGH_RISK_CAUTION, STATUS_DISCOVERY_INSUFFICIENT}


def _project_backend_dir() -> Path:
    return Path(__file__).resolve().parents[2]


class LocalMarketDiscoveryEngine:
    def __init__(self, output_dir: Path | None = None, provider: MarketDataProvider | None = None) -> None:
        self.output_dir = output_dir or (_project_backend_dir() / "data" / "discovery")
        self.history_dir = self.output_dir / "history"
        self.provider = provider

    def _provider(self) -> MarketDataProvider:
        if self.provider is not None:
            return self.provider
        from app.services.providers.provider_registry import get_active_provider

        return get_active_provider()

    def _discovery_freshness(self) -> DataFreshness:
        provider = self._provider()
        provider_status = provider.get_data_status()
        return DataFreshness(
            provider=provider.provider_name,
            source="local rule-based discovery over provider universe",
            as_of=provider_status.last_updated,
            age_minutes=provider.get_market_summary().data_freshness.age_minutes,
            is_stale=not provider_status.is_available,
            note="Discovery ใช้ provider mock/local และไม่ใช่ราคาจาก Dime โดยตรง",
        )

    def universe(self) -> list[LocalStockUniverseItem]:
        return self._provider().get_stock_universe()

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
            "ระบบเริ่มจากรายการหุ้นจำลองในเครื่องจาก provider layer",
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
            data_freshness=self._discovery_freshness(),
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
            result = DiscoveryRun.model_validate_json(latest_path.read_text(encoding="utf-8"))
        except (ValidationError, json.JSONDecodeError):
            return self.run(write_files=True)
        if self._should_regenerate(result):
            return self.run(write_files=True)
        return result

    def _should_regenerate(self, result: DiscoveryRun) -> bool:
        if not result.results:
            return True
        if result.data_freshness.source != "local rule-based discovery over provider universe":
            return True
        return any(item.category not in SUPPORTED_DISCOVERY_CATEGORIES for item in result.results)

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

    def get_stock_snapshot(self, symbol: str) -> StockSnapshot:
        item = self.get_universe_item(symbol)
        if item is None:
            return self._provider().get_stock_snapshot(symbol)
        return self.to_stock_snapshot(item)

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
