import os
from pathlib import Path
import tempfile

from fastapi.testclient import TestClient

_test_data_dir = tempfile.TemporaryDirectory()
os.environ["DIME_DB_PATH"] = str(Path(_test_data_dir.name) / "test_app.db")

from app.core.constants import (
    STATUS_DO_NOT_CHASE,
    STATUS_FOLLOW,
    STATUS_INSUFFICIENT_DATA,
    STATUS_PLAN_VALID,
    STATUS_PRICE_NOT_IN_ZONE,
)
from app.main import app
from app.schemas.contracts import JournalEntryCreate, RiskProfile, Zone
from app.services.discovery_engine import LocalMarketDiscoveryEngine
from app.services.providers.mock_provider import provider
from app.services.risk_engine import RiskEngine
from app.services.rule_engine import RuleEngine
from app.services.sqlite_store import SQLiteStore

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


def test_discovery_scoring_output_shape() -> None:
    engine = LocalMarketDiscoveryEngine(output_dir=Path(_test_data_dir.name) / "discovery_shape")
    result = engine.run(write_files=False)
    assert result.universe_count == 10
    assert result.disclaimer
    assert result.results[0].rank == 1
    assert result.results[0].final_score >= result.results[-1].final_score
    assert result.results[0].key_reasons
    assert result.results[0].caution_points
    assert result.results[0].explanation_trace
    assert result.results[0].data_freshness


def test_discovery_latest_endpoint_returns_ranked_results() -> None:
    response = client.get("/api/discovery/latest")
    assert response.status_code == 200
    payload = response.json()
    assert payload["universe_count"] == 10
    assert payload["results"][0]["rank"] == 1
    assert payload["results"][0]["final_score"] >= payload["results"][-1]["final_score"]
    assert payload["results"][0]["disclaimer"]


def test_discovery_run_endpoint_writes_latest_output() -> None:
    response = client.post("/api/discovery/run")
    assert response.status_code == 200
    payload = response.json()
    assert payload["results"]
    assert payload["data_freshness"]["provider"] == "local_discovery_mock"


def test_existing_radar_flow_uses_discovery_universe_compatibly() -> None:
    response = client.get("/api/radar")
    assert response.status_code == 200
    payload = response.json()
    symbols = [item["symbol"] for item in payload]
    assert "NVDA" in symbols
    assert "MSFT" in symbols
    assert len(payload) == 10
    assert payload[0]["score"] >= payload[-1]["score"]
    assert payload[0]["explanation_trace"]


def test_stock_explain_supports_new_discovery_symbol() -> None:
    response = client.get("/api/stocks/MSFT/explain")
    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "MSFT"
    assert payload["explanation_trace"]
    assert payload["reasons"]
    assert payload["cautions"]


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


def test_settings_values_survive_repository_reload() -> None:
    db_path = Path(_test_data_dir.name) / "settings_reload.db"
    first_store = SQLiteStore(db_path)
    payload = RiskProfile(
        beginner_level="confident",
        max_loss_per_trade_thb=2400,
        max_trades_per_day=4,
        minimum_risk_reward=2.2,
        preferred_setup_type="pullback-reload",
    )
    first_store.save_risk_profile(payload)

    second_store = SQLiteStore(db_path)
    assert second_store.get_risk_profile() == payload


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


def test_journal_entries_return_newest_first() -> None:
    first_payload = {
        "symbol": "AMD",
        "decision": "รอจังหวะ",
        "reason": "รายการเก่ากว่า",
        "result": "",
        "lesson_learned": "",
    }
    second_payload = {
        "symbol": "TSLA",
        "decision": "รอจังหวะ",
        "reason": "รายการใหม่กว่า",
        "result": "",
        "lesson_learned": "",
    }
    first = client.post("/api/journal", json=first_payload).json()
    second = client.post("/api/journal", json=second_payload).json()

    entries = client.get("/api/journal").json()
    ids = [entry["id"] for entry in entries]
    assert ids.index(second["id"]) < ids.index(first["id"])


def test_journal_entries_survive_repository_reload() -> None:
    db_path = Path(_test_data_dir.name) / "journal_reload.db"
    first_store = SQLiteStore(db_path)
    saved = first_store.create_journal_entry(
        entry=JournalEntryCreate(
            symbol="NVDA",
            decision="รอจังหวะ",
            reason="ทดสอบการเปิด repository ใหม่",
            result="",
            lesson_learned="ข้อมูลยังอยู่ใน SQLite",
        )
    )

    second_store = SQLiteStore(db_path)
    entries = second_store.list_journal_entries()
    assert entries[0].id == saved.id
    assert entries[0].symbol == "NVDA"


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
