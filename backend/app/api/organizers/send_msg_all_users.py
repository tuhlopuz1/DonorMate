from typing import Annotated

from app.api.tasks import send_msg
from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Notification, User
from app.models.schemas import MesagePayload, NotificationEnum, Role
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/send-msg-all-usr")
async def send_message_to_all_users(user: Annotated[User, Depends(check_user_token)], msg: MesagePayload):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    users = await adapter.get_all(User)
    for user in users:
        if user.role == Role.DONOR:
            send_msg.apply_async(kwargs={"chat_id": user.id, "text": msg.message})
            await adapter.insert(
                Notification, {"user_id": user.id, "type": NotificationEnum.INFO, "content": msg.message}
            )
    return okresponse()
