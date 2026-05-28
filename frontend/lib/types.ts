export type DataFreshness = {
  provider: string;
  source: string;
  as_of: string;
  age_minutes: number;
  is_stale: boolean;
  note: string;
};

export type StockSnapshot = {
  symbol: string;
  company_name: string;
  price: number;
  vwap: number;
  support: number;
  resistance: number;
  relative_volume: number;
  market_context: string;
  score: number;
  status: string;
  reasons: string[];
  cautions: string[];
  explanation_trace: string[];
  data_freshness: DataFreshness;
};

export type MarketSummary = {
  headline: string;
  tone: string;
  status: string;
  summary_th: string;
  indices: Record<string, number>;
  cautions: string[];
  data_freshness: DataFreshness;
  explanation_trace: string[];
};

export type DiscoveryResult = {
  symbol: string;
  name: string;
  sector_theme: string;
  beginner_summary: string;
  rank: number;
  final_score: number;
  category: string;
  key_reasons: string[];
  caution_points: string[];
  explanation_trace: string[];
  data_freshness: DataFreshness;
  disclaimer: string;
  mock_price: number;
  mock_daily_change_pct: number;
  trend_score: number;
  momentum_score: number;
  quality_score: number;
  valuation_risk_score: number;
  volatility_risk_score: number;
  liquidity_score: number;
  beginner_fit_score: number;
};

export type DiscoveryRun = {
  generated_at: string;
  universe_count: number;
  data_freshness: DataFreshness;
  disclaimer: string;
  results: DiscoveryResult[];
};

export type StockExplain = {
  stock: StockSnapshot;
  symbol: string;
  company_name: string;
  status: string;
  price: number;
  vwap: number;
  support: number;
  resistance: number;
  reasons: string[];
  cautions: string[];
  summary_th: string;
  important_zones: Record<string, number>;
  beginner_notes: string[];
  explanation_trace: string[];
  data_freshness: DataFreshness;
};

export type DimeCheckResponse = {
  symbol: string;
  dime_price: number;
  status: string;
  reason: string;
  action: string;
  risk_reward: number;
  passes_risk_profile: boolean;
  explanation_trace: string[];
  data_freshness: DataFreshness;
};

export type PracticePlan = {
  symbol: string;
  plan_type: string;
  entry_zone: { low: number; high: number };
  stop_loss: number;
  take_profit: number;
  risk_reward: number;
  max_position_size_shares: number;
  expected_loss_thb: number;
  expected_profit_thb: number;
  passes_risk_profile: boolean;
  status: string;
  disclaimer: string;
  reasons: string[];
  cautions: string[];
  explanation_trace: string[];
  data_freshness: DataFreshness;
};

export type RiskProfile = {
  beginner_level: "new" | "learning" | "confident";
  max_loss_per_trade_thb: number;
  max_trades_per_day: number;
  minimum_risk_reward: number;
  preferred_setup_type: string;
};

export type DataStatus = {
  provider: string;
  health: "healthy" | "degraded" | "unavailable";
  freshness: DataFreshness;
  message: string;
  limitations: string[];
  active_provider: string;
  provider_type: string;
  is_live_market_data_connected: boolean;
  is_dime_price_source_connected: boolean;
  has_trading_integration: boolean;
  is_discovery_local_rule_based: boolean;
  provider_status: {
    provider_available: boolean;
    provider_name: string;
    provider_type: string;
    is_available: boolean;
    is_live_data: boolean;
    is_direct_dime_data: boolean;
    is_degraded: boolean;
    fallback_used: boolean;
    fallback_reason: string;
    last_updated: string;
    freshness_label: string;
    limitations: string[];
    disclaimer: string;
    degraded_reason: string;
  };
};
