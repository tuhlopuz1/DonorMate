from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID

from app.api.tasks import send_msg
from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, emptyresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Event, Notification, Registration, User
from app.models.schemas import NotificationEnum, Role
from fastapi import APIRouter, Depends

router = APIRouter()


@router.delete("/event/{event_id}")
async def delete_event(user: Annotated[User, Depends(check_user_token)], event_id: UUID):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    event = await adapter.get_by_id(Event, event_id)
    if not event:
        return badresponse("Event not found", 404)
    now = datetime.now(timezone.utc)
    if event.start_date > now:
        regs = await adapter.get_by_value(Registration, "event_id", event_id)
        if regs:
            for reg in regs:
                await adapter.update_by_id(Registration, reg.id, {"notification": False})
                text = f"Мероприятие {event.name} было отменено."
                send_msg.apply_async(kwargs={"user_id": reg.user_id, "text": text})
                await adapter.insert(
                    Notification, {"user_id": reg.user_id, "type": NotificationEnum.ERROR, "content": text}
                )
    await adapter.delete(Event, event_id)
    return emptyresponse()
