from datetime import datetime, timezone

from app.schemas.contracts import Notification


class NotificationCenter:
    def list_notifications(self) -> list[Notification]:
        return [
            Notification(
                id=1,
                channel="in-app",
                title="โหมดข้อมูลจำลอง",
                message="ระบบ V1 ใช้ mock data เท่านั้น และไม่ใช่ราคาจาก Dime โดยตรง",
                created_at=datetime.now(timezone.utc),
            )
        ]
