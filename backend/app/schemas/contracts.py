from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class DataFreshness(BaseModel):
    provider: str
    source: str
    as_of: datetime
    age_minutes: int
    is_stale: bool
    note: str


class ProviderStatus(BaseModel):
    provider_name: str
    provider_type: str
    is_available: bool
    is_live_data: bool
    is_direct_dime_data: bool
    last_updated: datetime
    freshness_label: str
    limitations: list[str]
    disclaimer: str
    degraded_reason: str = ""


class Zone(BaseModel):
    low: float
    high: float


class StockSnapshot(BaseModel):
    symbol: str
    company_name: str
    price: float
    vwap: float
    support: float
    resistance: float
    relative_volume: float
    market_context: str
    score: int
    status: str
    reasons: list[str]
    cautions: list[str]
    explanation_trace: list[str]
    data_freshness: DataFreshness


class MarketSummary(BaseModel):
    headline: str
    tone: str
    status: str
    summary_th: str
    indices: dict[str, float]
    cautions: list[str]
    data_freshness: DataFreshness
    explanation_trace: list[str]


class LocalStockUniverseItem(BaseModel):
    symbol: str
    name: str
    sector_theme: str
    mock_price: float
    mock_daily_change_pct: float
    trend_score: int
    momentum_score: int
    quality_score: int
    valuation_risk_score: int
    volatility_risk_score: int
    liquidity_score: int
    beginner_fit_score: int
    beginner_description: str
    data_status: str
    vwap: float
    support: float
    resistance: float
    relative_volume: float
    data_freshness: DataFreshness


class DiscoveryResult(BaseModel):
    symbol: str
    name: str
    sector_theme: str
    beginner_summary: str
    rank: int
    final_score: int
    category: str
    key_reasons: list[str]
    caution_points: list[str]
    explanation_trace: list[str]
    data_freshness: DataFreshness
    disclaimer: str
    mock_price: float
    mock_daily_change_pct: float
    trend_score: int
    momentum_score: int
    quality_score: int
    valuation_risk_score: int
    volatility_risk_score: int
    liquidity_score: int
    beginner_fit_score: int


class DiscoveryRun(BaseModel):
    generated_at: datetime
    universe_count: int
    data_freshness: DataFreshness
    disclaimer: str
    results: list[DiscoveryResult]


class RiskProfile(BaseModel):
    beginner_level: Literal["new", "learning", "confident"] = "new"
    max_loss_per_trade_thb: float = Field(default=1000, gt=0)
    max_trades_per_day: int = Field(default=2, ge=1)
    minimum_risk_reward: float = Field(default=1.5, gt=0)
    preferred_setup_type: str = "pullback"


class PracticePlan(BaseModel):
    symbol: str
    plan_type: str
    entry_zone: Zone
    stop_loss: float
    take_profit: float
    risk_reward: float
    max_position_size_shares: int
    expected_loss_thb: float
    expected_profit_thb: float
    passes_risk_profile: bool
    status: str
    disclaimer: str
    reasons: list[str]
    cautions: list[str]
    explanation_trace: list[str]
    data_freshness: DataFreshness


class DimeCheckRequest(BaseModel):
    symbol: str
    dime_price: float = Field(gt=0)
    entry_zone: Zone | None = None
    stop_loss: float | None = None
    take_profit: float | None = None


class DimeCheckResponse(BaseModel):
    symbol: str
    dime_price: float
    status: str
    reason: str
    action: str
    risk_reward: float
    passes_risk_profile: bool
    explanation_trace: list[str]
    data_freshness: DataFreshness


class JournalEntryCreate(BaseModel):
    symbol: str
    decision: str
    reason: str
    result: str = ""
    lesson_learned: str = ""

    @field_validator("symbol", "decision")
    @classmethod
    def required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("required")
        return cleaned

    @field_validator("reason", "result", "lesson_learned")
    @classmethod
    def clean_optional_text(cls, value: str) -> str:
        return value.strip()

    @model_validator(mode="after")
    def reason_or_lesson_required(self) -> "JournalEntryCreate":
        if not self.reason and not self.lesson_learned:
            raise ValueError("reason or lesson_learned is required")
        self.symbol = self.symbol.upper()
        return self


class JournalEntry(JournalEntryCreate):
    id: int
    created_at: datetime


class DataStatus(BaseModel):
    provider: str
    health: Literal["healthy", "degraded", "unavailable"]
    freshness: DataFreshness
    message: str
    limitations: list[str]
    active_provider: str
    provider_type: str
    is_live_market_data_connected: bool
    is_dime_price_source_connected: bool
    has_trading_integration: bool
    is_discovery_local_rule_based: bool
    provider_status: ProviderStatus


class Notification(BaseModel):
    id: int
    channel: str
    title: str
    message: str
    created_at: datetime
    read: bool = False
