from fastapi import APIRouter

from app.core.config import settings
from app.schemas.contracts import DimeCheckRequest, DimeCheckResponse, RiskProfile
from app.services.discovery_engine import discovery_engine
from app.services.risk_engine import RiskEngine
from app.services.rule_engine import RuleEngine
from app.api.stocks import _plan_zones

router = APIRouter(tags=["dime"])
rule_engine = RuleEngine()
risk_engine = RiskEngine(settings.assumed_usd_thb)


@router.post("/dime/check-price", response_model=DimeCheckResponse)
def check_dime_price(payload: DimeCheckRequest) -> DimeCheckResponse:
    stock = discovery_engine.get_stock_snapshot(payload.symbol)
    default_entry_zone, default_stop_loss, default_take_profit = _plan_zones(stock.symbol)
    entry_zone = payload.entry_zone or default_entry_zone
    stop_loss = payload.stop_loss or default_stop_loss
    take_profit = payload.take_profit or default_take_profit
    result = rule_engine.check_dime_price(
        symbol=stock.symbol,
        dime_price=payload.dime_price,
        entry_zone=entry_zone,
        stop_loss=stop_loss,
        take_profit=take_profit,
        profile=RiskProfile(),
        freshness=stock.data_freshness,
        risk_engine=risk_engine,
    )
    return DimeCheckResponse(symbol=stock.symbol, dime_price=payload.dime_price, data_freshness=stock.data_freshness, **result)
