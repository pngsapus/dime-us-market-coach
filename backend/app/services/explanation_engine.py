from app.schemas.contracts import PracticePlan, StockSnapshot


class ExplanationEngine:
    def explain_stock(self, stock: StockSnapshot) -> dict:
        return {
            "summary_th": (
                f"{stock.symbol} ({stock.company_name}) อยู่ในสถานะ {stock.status} "
                f"เพราะระบบเห็นราคาเทียบกับ VWAP, แนวรับแนวต้าน และปริมาณซื้อขายสัมพันธ์ร่วมกัน"
            ),
            "important_zones": {
                "support": stock.support,
                "resistance": stock.resistance,
                "vwap": stock.vwap,
            },
            "beginner_notes": [
                "VWAP ใช้ดูว่าราคาปัจจุบันอยู่เหนือหรือต่ำกว่าราคาเฉลี่ยถ่วงน้ำหนักของวัน",
                "แนวรับและแนวต้านเป็นโซนสังเกต ไม่ใช่ราคาที่รับประกัน",
                "ควรตรวจสอบราคาจริงใน Dime ก่อนใช้แผนวิเคราะห์จำลอง",
            ],
            "explanation_trace": stock.explanation_trace,
        }

    def explain_plan(self, plan: PracticePlan) -> list[str]:
        return [
            f"กำหนด entry zone จากแนวรับและ VWAP ของ {plan.symbol}",
            f"คำนวณ Risk:Reward จากจุดกลาง entry zone, stop loss และ take profit",
            f"เทียบความเสี่ยงกับ risk profile แล้ว passes_risk_profile={plan.passes_risk_profile}",
        ]
