from fastapi import APIRouter

from app.schemas.contracts import StockSnapshot
from app.services.discovery_engine import discovery_engine

router = APIRouter(tags=["radar"])


@router.get("/radar", response_model=list[StockSnapshot])
def get_radar() -> list[StockSnapshot]:
    latest = discovery_engine.latest()
    ranked_symbols = [item.symbol for item in latest.results]
    stocks_by_symbol = {stock.symbol: stock for stock in [discovery_engine.get_stock_snapshot(symbol) for symbol in ranked_symbols]}
    return [stocks_by_symbol[symbol] for symbol in ranked_symbols if symbol in stocks_by_symbol]
