from uuid import UUID
from datetime import datetime, timezone, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends
from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import User, Event, Registration
from app.api.events.tasks import schedule_telegram_message

router = APIRouter()


@router.post("/register-on-event/{event_id}")
async def register_on_event(user: Annotated[User, Depends(check_user_token)], event_id: UUID, notif: bool = True):
    if not user:
        return badresponse("Unauthorized", 401)
    event = await adapter.get_by_id(Event, event_id)
    if not event:
        return badresponse("Event not found", 404)
    if event.registred > event.max_donors:
        return badresponse("No more vacant places", 403)
    now = datetime.now(timezone.utc)
    if event.end_date < now:
        return badresponse("Event ended", 403)
    registration = await adapter.insert(
        Registration,
        {
            "user_id": user.id,
            "event_id": event_id,
            "notification": notif
        }
    )
    text = ""
    if event.start_data > now:
        eta1 = event.start_data
        eta2 = eta1 - timedelta(hours=1)
        if notif:
            schedule_telegram_message.apply_async(
                kwargs={"text": text, "chat_id": user.id, },
                eta=eta2,
            )
            if eta2 > now:
                schedule_telegram_message.apply_async(
                    kwargs={"text": text, "chat_id": user.id, },
                    eta=eta2,
                )
    await adapter.update_by_id(Event, event_id, {"registred": event.registred + 1})
    return okresponse(registration.id)
