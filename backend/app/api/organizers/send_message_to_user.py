from typing import Annotated

from app.api.tasks import send_msg
from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Notification, User
from app.models.schemas import MesagePayload, NotificationEnum, Role
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/send-message/{id}")
async def find_user(user: Annotated[User, Depends(check_user_token)], id: int, msg: MesagePayload):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    reciever = await adapter.get_by_id(User, id)
    if not reciever:
        return badresponse("User not found", 404)
    await adapter.insert(Notification, {"user_id": id, "type": NotificationEnum.INFO, "content": msg.message})
    send_msg.apply_async(kwargs={"chat_id": id, "text": msg.message}, countdown=0.0)
    return okresponse()
