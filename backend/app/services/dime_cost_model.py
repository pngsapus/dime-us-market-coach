class DimeCostModel:
    def estimate_placeholder(self, gross_amount_usd: float) -> dict:
        return {
            "gross_amount_usd": gross_amount_usd,
            "estimated_fee_usd": 0.0,
            "note": "Placeholder only. ยังไม่ได้เชื่อมต่อหรือยืนยันโครงสร้างค่าธรรมเนียมจริงของ Dime",
        }
