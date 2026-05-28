from fastapi import APIRouter

from app.core.config import settings
from app.core.constants import STATUS_INSUFFICIENT_DATA, STATUS_WAIT
from app.schemas.contracts import PracticePlan, RiskProfile, Zone
from app.services.explanation_engine import ExplanationEngine
from app.services.providers.mock_provider import provider
from app.services.risk_engine import RiskEngine

router = APIRouter(tags=["stocks"])
risk_engine = RiskEngine(settings.assumed_usd_thb)
explanation_engine = ExplanationEngine()


def _default_profile() -> RiskProfile:
    return RiskProfile()


def _plan_zones(symbol: str, support: float | None = None, resistance: float | None = None, vwap: float | None = None) -> tuple[Zone, float, float]:
    zones = {
        "NVDA": (Zone(low=129.0, high=132.5), 126.0, 144.0),
        "AMD": (Zone(low=160.0, high=164.5), 156.5, 172.0),
        "TSLA": (Zone(low=174.0, high=178.5), 169.5, 188.0),
    }
    if symbol.upper() in zones:
        return zones[symbol.upper()]
    if support is None or resistance is None or vwap is None:
        return zones["NVDA"]
    entry_low = round(max(support, vwap * 0.99), 2)
    entry_high = round(max(entry_low + 0.01, min(vwap * 1.01, resistance * 0.98)), 2)
    stop_loss = round(support * 0.98, 2)
    take_profit = round(resistance, 2)
    return Zone(low=entry_low, high=entry_high), stop_loss, take_profit


@router.get("/stocks/{symbol}/explain")
def explain_stock(symbol: str) -> dict:
    evaluated = provider.get_stock(symbol)
    explanation = explanation_engine.explain_stock(evaluated)
    return {
        "stock": evaluated,
        "symbol": evaluated.symbol,
        "company_name": evaluated.company_name,
        "status": evaluated.status,
        "price": evaluated.price,
        "vwap": evaluated.vwap,
        "support": evaluated.support,
        "resistance": evaluated.resistance,
        "reasons": evaluated.reasons,
        "cautions": evaluated.cautions,
        "data_freshness": evaluated.data_freshness,
        **explanation,
    }


@router.get("/stocks/{symbol}/practice-plan", response_model=PracticePlan)
def get_practice_plan(symbol: str) -> PracticePlan:
    stock = provider.get_stock(symbol)
    entry_zone, stop_loss, take_profit = _plan_zones(stock.symbol, stock.support, stock.resistance, stock.vwap)
    profile = _default_profile()
    risk = risk_engine.calculate_plan(entry_zone, stop_loss, take_profit, profile)
    status = STATUS_INSUFFICIENT_DATA if stock.data_freshness.is_stale else STATUS_WAIT
    plan = PracticePlan(
        symbol=stock.symbol,
        plan_type="แผนวิเคราะห์จำลอง",
        entry_zone=entry_zone,
        stop_loss=stop_loss,
        take_profit=take_profit,
        risk_reward=risk["risk_reward"],
        max_position_size_shares=risk["max_position_size_shares"],
        expected_loss_thb=risk["expected_loss_thb"],
        expected_profit_thb=risk["expected_profit_thb"],
        passes_risk_profile=risk["passes_risk_profile"] and not stock.data_freshness.is_stale,
        status=status,
        disclaimer="แผนนี้เป็นการจำลองเพื่อฝึกวิเคราะห์ ไม่ใช่คำสั่งซื้อขาย",
        reasons=[
            "ใช้โซนราคาใกล้แนวรับและ VWAP จาก mock data",
            "คำนวณขนาดสถานะจาก max loss per trade ใน risk profile",
        ],
        cautions=[
            "ต้องตรวจสอบราคาจริงใน Dime ก่อนใช้ประกอบการพิจารณา",
            "หากราคาจริงออกนอกโซน แผนจำลองอาจไม่อยู่ในเกณฑ์",
        ],
        explanation_trace=[],
        data_freshness=stock.data_freshness,
    )
    return plan.model_copy(update={"explanation_trace": stock.explanation_trace + explanation_engine.explain_plan(plan)})
