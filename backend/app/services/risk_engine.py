from app.schemas.contracts import RiskProfile, Zone


class RiskEngine:
    def __init__(self, usd_thb: float = 36.5) -> None:
        self.usd_thb = usd_thb

    def calculate_risk_reward(self, entry_price: float, stop_loss: float, take_profit: float) -> float:
        risk_per_share = entry_price - stop_loss
        reward_per_share = take_profit - entry_price
        if risk_per_share <= 0 or reward_per_share <= 0:
            return 0.0
        return round(reward_per_share / risk_per_share, 2)

    def calculate_plan(self, entry_zone: Zone, stop_loss: float, take_profit: float, profile: RiskProfile) -> dict:
        planned_entry = round((entry_zone.low + entry_zone.high) / 2, 2)
        risk_usd = max(planned_entry - stop_loss, 0)
        reward_usd = max(take_profit - planned_entry, 0)
        risk_thb_per_share = risk_usd * self.usd_thb
        max_position_size = int(profile.max_loss_per_trade_thb // risk_thb_per_share) if risk_thb_per_share > 0 else 0
        risk_reward = self.calculate_risk_reward(planned_entry, stop_loss, take_profit)
        expected_loss = round(max_position_size * risk_thb_per_share, 2)
        expected_profit = round(max_position_size * reward_usd * self.usd_thb, 2)
        return {
            "planned_entry": planned_entry,
            "risk_reward": risk_reward,
            "max_position_size_shares": max_position_size,
            "expected_loss_thb": expected_loss,
            "expected_profit_thb": expected_profit,
            "passes_risk_profile": risk_reward >= profile.minimum_risk_reward and max_position_size > 0,
        }
