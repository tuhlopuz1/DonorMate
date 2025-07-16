from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID

from app.api.events.tasks import schedule_telegram_message
from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.dependencies.token_manager import TokenManager
from app.models.db_adapter import adapter
from app.models.db_tables import Event, Registration, User
from fastapi import APIRouter, Depends

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
    org = await adapter.get_by_id(User, event.organizer)
    registration = await adapter.insert(Registration, {"user_id": user.id, "event_id": event_id, "notification": notif})
    if event.start_data > now:
        eta1 = event.start_data - timedelta(minutes=10)
        eta2 = event.start_data - timedelta(hours=1)
        expiration = (event.end_data - now).total_seconds()
        access_qr_token = TokenManager.encode_qr_token({"iss": str(user.id), "sub": str(registration.id)}, expiration)
        event_name = event.name if event.name is not None else ""
        if notif and user.notifications_bool:
            schedule_telegram_message.apply_async(
                kwargs={
                    "text": (
                        f"Ваша запись на мероприятие {event_name} состоится через 10 минут!",  # noqa
                        f"\nПодойдите в: {event.place}, ",
                        f"\nДля связи с организатором пишите в телеграмм: @{org.username}",
                        "\nНа входе покажите QR-код (действителен до конца мероприятия)",
                    ),
                    "chat_id": user.id,
                    "reg_id": registration.id,
                    "data": access_qr_token,
                },
                eta=eta1,
            )
            if eta2 > now:
                schedule_telegram_message.apply_async(
                    kwargs={
                        "text": (
                            f"Ваша запись на мероприятие {event_name} состоится через час!",  # noqa
                            f"\nПриходить в: {event.place}, ",
                            f"\nДля связи с организатором пишите в телеграмм: @{org.username}",
                            "За 10 минут до записи вам придёт QR-код (нужен для входа на площадку)",
                        ),
                        "chat_id": user.id,
                        "reg_id": registration.id,
                    },
                    eta=eta2,
                )
    await adapter.update_by_id(Event, event_id, {"registred": event.registred + 1})
    return okresponse(registration.id)
