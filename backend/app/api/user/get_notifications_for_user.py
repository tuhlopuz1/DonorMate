from datetime import datetime, timezone
from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Notification, User
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/get-notifications-for-user")
async def get_notifications_for_users(user: Annotated[User, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    user_notifications = await adapter.get_by_cond(
        Notification, "user_id", user.id, "==", "time_to_invalid", datetime.now(timezone.utc), "<"
    )
    return user_notifications
