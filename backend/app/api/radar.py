from fastapi import APIRouter

from app.schemas.contracts import StockSnapshot
from app.services.providers.mock_provider import provider
from app.services.rule_engine import RuleEngine

router = APIRouter(tags=["radar"])
rule_engine = RuleEngine()


@router.get("/radar", response_model=list[StockSnapshot])
def get_radar() -> list[StockSnapshot]:
    results: list[StockSnapshot] = []
    for stock in provider.list_stocks():
        rule_result = rule_engine.evaluate_stock(stock)
        results.append(
            stock.model_copy(
                update={
                    "status": rule_result["status"],
                    "score": rule_result["score"],
                    "reasons": rule_result["reasons"],
                    "cautions": rule_result["cautions"],
                    "explanation_trace": stock.explanation_trace + rule_result["explanation_trace"],
                }
            )
        )
    return results
