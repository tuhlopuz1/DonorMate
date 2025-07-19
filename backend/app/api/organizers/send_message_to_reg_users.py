from typing import Annotated
from uuid import UUID

from app.api.tasks import send_msg
from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Notification, Registration, User
from app.models.schemas import MesagePayload, NotificationEnum, Role
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/send-msg-all-usr/{event_id}")
async def send_message_to_all_users(
    user: Annotated[User, Depends(check_user_token)], event_id: UUID, msg: MesagePayload
):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    regs = await adapter.get_by_value(Registration, "event_id", event_id)
    for reg in regs:
        send_msg.apply_async(kwargs={"chat_id": reg.user_id, "text": msg.message})
        await adapter.insert(
            Notification, {"user_id": reg.user_id, "type": NotificationEnum.INFO, "content": msg.message}
        )
    return okresponse()
