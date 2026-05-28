from fastapi import APIRouter

from app.schemas.contracts import Notification
from app.services.notification_center import NotificationCenter

router = APIRouter(tags=["notifications"])
notification_center = NotificationCenter()


@router.get("/notifications", response_model=list[Notification])
def get_notifications() -> list[Notification]:
    return notification_center.list_notifications()
