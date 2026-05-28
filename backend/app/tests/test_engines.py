from fastapi.testclient import TestClient

from app.core.constants import (
    STATUS_DO_NOT_CHASE,
    STATUS_FOLLOW,
    STATUS_INSUFFICIENT_DATA,
    STATUS_PLAN_VALID,
    STATUS_PRICE_NOT_IN_ZONE,
)
from app.main import app
from app.schemas.contracts import RiskProfile, Zone
from app.services.providers.mock_provider import provider
from app.services.risk_engine import RiskEngine
from app.services.rule_engine import RuleEngine

client = TestClient(app)


def test_risk_reward_calculation() -> None:
    engine = RiskEngine()
    assert engine.calculate_risk_reward(entry_price=100, stop_loss=95, take_profit=112.5) == 2.5


def test_dime_price_above_entry_zone_warns_do_not_chase() -> None:
    stock = provider.get_stock("NVDA")
    result = RuleEngine().check_dime_price(
        symbol="NVDA",
        dime_price=134.0,
        entry_zone=Zone(low=129.0, high=132.5),
        stop_loss=126.0,
        take_profit=144.0,
        profile=RiskProfile(),
        freshness=stock.data_freshness,
        risk_engine=RiskEngine(),
    )
    assert result["status"] == STATUS_DO_NOT_CHASE
    assert result["passes_risk_profile"] is False


def test_stock_explain_endpoint_returns_explanation_trace() -> None:
    response = client.get("/api/stocks/NVDA/explain")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"]
    assert payload["data_freshness"]
    assert payload["explanation_trace"]
    assert payload["reasons"]
    assert payload["cautions"]


def test_practice_plan_endpoint_returns_valid_plan_data() -> None:
    response = client.get("/api/stocks/NVDA/practice-plan")
    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "NVDA"
    assert payload["entry_zone"]["low"] < payload["entry_zone"]["high"]
    assert payload["stop_loss"] < payload["entry_zone"]["low"]
    assert payload["take_profit"] > payload["entry_zone"]["high"]
    assert payload["risk_reward"] >= 1.5
    assert payload["data_freshness"]
    assert payload["explanation_trace"]


def test_dime_check_above_entry_zone_endpoint_returns_do_not_chase() -> None:
    response = client.post("/api/dime/check-price", json={"symbol": "NVDA", "dime_price": 134.0})
    assert response.status_code == 200
    assert response.json()["status"] == STATUS_DO_NOT_CHASE


def test_dime_check_inside_entry_zone_endpoint_returns_plan_valid() -> None:
    response = client.post("/api/dime/check-price", json={"symbol": "NVDA", "dime_price": 131.0})
    assert response.status_code == 200
    assert response.json()["status"] == STATUS_PLAN_VALID


def test_dime_check_below_entry_zone_endpoint_returns_price_not_in_zone() -> None:
    response = client.post("/api/dime/check-price", json={"symbol": "NVDA", "dime_price": 128.0})
    assert response.status_code == 200
    assert response.json()["status"] == STATUS_PRICE_NOT_IN_ZONE


def test_rule_engine_follow_when_price_above_vwap_and_rvol_high() -> None:
    stock = provider.get_stock("NVDA")
    result = RuleEngine().evaluate_stock(stock)
    assert result["status"] == STATUS_FOLLOW


def test_rule_engine_insufficient_when_data_is_stale() -> None:
    stock = provider.get_stock("TSLA")
    result = RuleEngine().evaluate_stock(stock)
    assert result["status"] == STATUS_INSUFFICIENT_DATA
    assert result["score"] <= 40
    assert result["cautions"]


def test_explanation_trace_exists_for_every_analysis_result() -> None:
    rule_engine = RuleEngine()
    for stock in provider.list_stocks():
        result = rule_engine.evaluate_stock(stock)
        assert result["explanation_trace"]
        assert stock.explanation_trace


def test_settings_post_saves_values_and_get_returns_updated_values() -> None:
    payload = {
        "beginner_level": "learning",
        "max_loss_per_trade_thb": 1500.5,
        "max_trades_per_day": 3,
        "minimum_risk_reward": 2.0,
        "preferred_setup_type": "pullback",
    }
    post_response = client.post("/api/settings/risk-profile", json=payload)
    assert post_response.status_code == 200
    get_response = client.get("/api/settings/risk-profile")
    assert get_response.status_code == 200
    assert get_response.json() == payload


def test_journal_post_creates_entry_and_get_returns_it() -> None:
    payload = {
        "symbol": "nvda",
        "decision": "รอจังหวะ",
        "reason": "ราคายังต้องรอเข้ากรอบแผน",
        "result": "",
        "lesson_learned": "ต้องตรวจสอบ Risk:Reward ก่อนตัดสินใจเอง",
    }
    post_response = client.post("/api/journal", json=payload)
    assert post_response.status_code == 200
    saved = post_response.json()
    assert saved["symbol"] == "NVDA"
    assert saved["decision"] == payload["decision"]
    get_response = client.get("/api/journal")
    assert get_response.status_code == 200
    assert any(entry["id"] == saved["id"] for entry in get_response.json())


def test_journal_validation_rejects_missing_required_fields() -> None:
    missing_symbol = client.post(
        "/api/journal",
        json={"symbol": "", "decision": "รอจังหวะ", "reason": "มีเหตุผล", "result": "", "lesson_learned": ""},
    )
    assert missing_symbol.status_code == 422

    missing_reason_and_lesson = client.post(
        "/api/journal",
        json={"symbol": "NVDA", "decision": "รอจังหวะ", "reason": "", "result": "", "lesson_learned": ""},
    )
    assert missing_reason_and_lesson.status_code == 422
