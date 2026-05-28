# Rule Engine

Rule decisions are deterministic and based on explicit inputs.

## Stock Status Rules

- If `data_freshness.is_stale` is true, status is `ข้อมูลไม่เพียงพอ`.
- If price is above VWAP and relative volume is at least `1.4`, status is `ควรติดตาม`.
- If price is at or below VWAP, status is `รอจังหวะ`.
- Otherwise status remains `รอจังหวะ` until confirmation is stronger.

## Dime Check Rules

- If provider data is stale, status is `ข้อมูลไม่เพียงพอ`.
- If user-entered Dime price is above the entry zone, status is `ไม่ควรไล่ซื้อ`.
- If user-entered Dime price is below the entry zone, status is `แผนยกเลิก`.
- If price is inside the entry zone but Risk:Reward is below profile minimum, status is `ไม่ควรไล่ซื้อ`.
- If price is inside the entry zone and Risk:Reward passes, status is `แผนยังอยู่ในเกณฑ์`.
