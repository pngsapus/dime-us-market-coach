from app.core.constants import (
    STATUS_DO_NOT_CHASE,
    STATUS_FOLLOW,
    STATUS_INSUFFICIENT_DATA,
    STATUS_PLAN_CANCELLED,
    STATUS_PLAN_VALID,
    STATUS_PRICE_NOT_IN_ZONE,
    STATUS_WAIT,
)
from app.schemas.contracts import DataFreshness, RiskProfile, StockSnapshot, Zone
from app.services.risk_engine import RiskEngine


class RuleEngine:
    def evaluate_stock(self, stock: StockSnapshot) -> dict:
        trace: list[str] = []
        if stock.data_freshness.is_stale:
            trace.append("ข้อมูลถูกระบุว่า stale จึงไม่ใช้สรุปเป็นแผนติดตาม")
            return {
                "status": STATUS_INSUFFICIENT_DATA,
                "score": min(stock.score, 40),
                "reasons": ["ข้อมูลไม่สดพอสำหรับการวิเคราะห์"],
                "cautions": ["ควรรอข้อมูลชุดใหม่ก่อนประเมิน"],
                "explanation_trace": trace,
            }

        trace.append(f"ราคา {stock.price} เทียบกับ VWAP {stock.vwap}")
        trace.append(f"Relative Volume เท่ากับ {stock.relative_volume}")
        if stock.price > stock.vwap and stock.relative_volume >= 1.4:
            return {
                "status": STATUS_FOLLOW,
                "score": max(stock.score, 75),
                "reasons": ["ราคาอยู่เหนือ VWAP", "ปริมาณซื้อขายสัมพันธ์สูงกว่าปกติ"],
                "cautions": ["ควรรอให้ราคาอยู่ใกล้โซนแผน ไม่ไล่ราคาที่ขยับแรงแล้ว"],
                "explanation_trace": trace + ["เข้าเงื่อนไข momentum-follow แบบติดตาม"],
            }
        if stock.price <= stock.vwap:
            return {
                "status": STATUS_WAIT,
                "score": min(stock.score, 65),
                "reasons": ["ราคายังไม่ยืนเหนือ VWAP"],
                "cautions": ["รอให้โครงสร้างราคาชัดขึ้น"],
                "explanation_trace": trace + ["ยังไม่ผ่านเงื่อนไขติดตามหลัก"],
            }
        return {
            "status": STATUS_WAIT,
            "score": stock.score,
            "reasons": ["มีบางปัจจัยน่าสนใจ แต่แรงยืนยันยังไม่ครบ"],
            "cautions": ["ตรวจสอบราคาจริงใน Dime ก่อนใช้แผนจำลอง"],
            "explanation_trace": trace + ["เงื่อนไขติดตามยังไม่ครบทั้งหมด"],
        }

    def check_dime_price(
        self,
        symbol: str,
        dime_price: float,
        entry_zone: Zone,
        stop_loss: float,
        take_profit: float,
        profile: RiskProfile,
        freshness: DataFreshness,
        risk_engine: RiskEngine,
    ) -> dict:
        rr = risk_engine.calculate_risk_reward(dime_price, stop_loss, take_profit)
        trace = [
            f"ราคาจริงที่ผู้ใช้กรอกใน Dime คือ {dime_price}",
            f"โซนแผนเดิมคือ {entry_zone.low} ถึง {entry_zone.high}",
            f"Risk:Reward คำนวณใหม่ได้ {rr}",
        ]
        if freshness.is_stale:
            return {
                "status": STATUS_INSUFFICIENT_DATA,
                "reason": "ข้อมูลประกอบแผนไม่สดพอ จึงไม่ควรสรุปว่าแผนยังใช้ได้",
                "action": "รอข้อมูลใหม่และตรวจสอบราคาจริงอีกครั้ง",
                "risk_reward": rr,
                "passes_risk_profile": False,
                "explanation_trace": trace + ["ข้อมูล freshness เป็น stale"],
            }
        if dime_price > entry_zone.high:
            return {
                "status": STATUS_DO_NOT_CHASE,
                "reason": "ราคาจริงใน Dime สูงกว่าโซนเข้าที่วางไว้แล้ว ทำให้ Risk:Reward แย่ลง",
                "action": "รอจังหวะใหม่",
                "risk_reward": rr,
                "passes_risk_profile": False,
                "explanation_trace": trace + ["ราคาสูงกว่า entry zone จึงไม่ควรไล่ราคา"],
            }
        if dime_price < entry_zone.low:
            return {
                "status": STATUS_PRICE_NOT_IN_ZONE,
                "reason": "ราคาจริงใน Dime ยังต่ำกว่าโซนที่วางแผนไว้ จึงยังไม่เข้าเงื่อนไขของแผนจำลอง",
                "action": "รอให้ราคาและข้อมูลประกอบกลับมาอยู่ในเกณฑ์ก่อนประเมินใหม่",
                "risk_reward": rr,
                "passes_risk_profile": False,
                "explanation_trace": trace + ["ราคายังต่ำกว่า entry zone จึงยังไม่เข้าโซนแผน"],
            }
        if rr < profile.minimum_risk_reward:
            return {
                "status": STATUS_DO_NOT_CHASE,
                "reason": "ราคายังอยู่ในโซน แต่ Risk:Reward ต่ำกว่าเกณฑ์ของผู้ใช้",
                "action": "รอจังหวะใหม่",
                "risk_reward": rr,
                "passes_risk_profile": False,
                "explanation_trace": trace + ["Risk:Reward ต่ำกว่า minimum profile"],
            }
        return {
            "status": STATUS_PLAN_VALID,
            "reason": "ราคายังอยู่ในโซนที่วางแผนไว้",
            "action": "ใช้เพื่อประกอบการพิจารณาเท่านั้น ไม่ใช่คำสั่งซื้อ",
            "risk_reward": rr,
            "passes_risk_profile": True,
            "explanation_trace": trace + ["ราคาอยู่ใน entry zone และผ่านเกณฑ์ risk profile"],
        }
