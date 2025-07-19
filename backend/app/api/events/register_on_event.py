from datetime import datetime, timedelta, timezone  # noqa
from typing import Annotated
from uuid import UUID

from app.api.tasks import schedule_telegram_message, schedule_telegram_qr
from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.dependencies.token_manager import TokenManager
from app.models.db_adapter import adapter
from app.models.db_tables import Event, Notification, Registration, User
from app.models.schemas import NotificationEnum
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/register-on-event/{event_id}")
async def register_on_event(user: Annotated[User, Depends(check_user_token)], event_id: UUID, notif: bool = True):
    if not user:
        return badresponse("Unauthorized", 401)
    event = await adapter.get_by_id(Event, event_id)
    if not event:
        return badresponse("Event not found", 404)
    now = datetime.now(timezone.utc)
    if event.end_date < now:
        return badresponse("Event ended", 403)
    registration = await adapter.insert(Registration, {"user_id": user.id, "event_id": event_id, "notification": notif})
    if event.start_date > now:
        eta1 = event.start_date - timedelta(hours=1)
        eta2 = event.start_date - timedelta(days=1)
        eta3 = event.start_date - timedelta(days=3)
        eta4 = event.start_date - timedelta(days=7)
        expiration = (event.end_date - now).total_seconds()
        access_qr_token = TokenManager.encode_qr_token({"iss": str(user.id), "sub": str(registration.id)}, expiration)
        event_name = event.name if event.name is not None else ""
        if eta1 < now and event.end_date > now:
            schedule_telegram_qr.apply_async(
                kwargs={
                    "text": (
                        f"Ваша запись {event.name} активна прямо сейчас! Спешите!",
                        f"\nВам нужно подойти в {event.place}",
                        "\nЕсли понадобится, на входе покажите организатору этот QR-код",
                    ),
                    "chat_id": user.id,
                    "reg_id": registration.id,
                    "data": access_qr_token,
                },
                countdown=0.0,
            )
            await adapter.insert(
                Notification,
                {"user_id": user.id, "type": NotificationEnum.ERROR, "content": "lol"},
            )
        if notif and user.notifications_bool:
            if eta1 > now:
                schedule_telegram_qr.apply_async(
                    kwargs={
                        "text": (
                            f'Ваша запись на мероприятие "{event_name}" состоится через час!',
                            f"\nПодойдите в: {event.place}, ",
                            "\nДля связи с организатором пишите в этот чат интересующие вас вопросы,",
                            "либо воспользуйтесь формой в МиниПриложении"
                            "\nЕсли понадобится, на входе покажите организатору этот QR-код",
                        ),
                        "chat_id": user.id,
                        "reg_id": registration.id,
                        "data": access_qr_token,
                    },
                    eta=eta1,
                )
                await adapter.insert(
                    Notification,
                    {"user_id": user.id, "type": NotificationEnum.WARNING, "date_to_valid": eta1, "content": "lol"},
                )
            if eta2 > now:
                schedule_telegram_message.apply_async(
                    kwargs={
                        "text": (
                            f"Ваша запись на мероприятие {event_name} состоится уже завтра!",
                            f"\nПриходить в: {event.place}, ",
                            "\nДля связи с организатором пишите в этот чат интересующие вас вопросы,",
                            "либо воспользуйтесь формой в МиниПриложении",
                        ),
                        "chat_id": user.id,
                        "reg_id": registration.id,
                    },
                    eta=eta2,
                )
                await adapter.insert(
                    Notification,
                    {"user_id": user.id, "type": NotificationEnum.INFO, "date_to_valid": eta2, "content": "lol"},
                )
            if eta3 > now:
                schedule_telegram_message.apply_async(
                    kwargs={
                        "text": (
                            f"Ваша запись на мероприятие {event_name} состоится через три дня!",
                            "\nНапоминаем, что за двое суток до сдачи нельзя принимать алкоголь,",
                            "\nа так же необходимо отказаться от любых лекарств (в т. ч. анальгетиков),",
                            "\nДля связи с организатором пишите в этот чат интересующие вас вопросы,",
                            "либо воспользуйтесь формой в МиниПриложении",
                        ),
                        "chat_id": user.id,
                        "reg_id": registration.id,
                    },
                    eta=eta3,
                )
                await adapter.insert(
                    Notification,
                    {"user_id": user.id, "type": NotificationEnum.INFO, "date_to_valid": eta3, "content": "lol"},
                )
            if eta4 > now:
                schedule_telegram_message.apply_async(
                    kwargs={
                        "text": (
                            f"Ваша запись на мероприятие {event_name} состоится через неделю.",
                            f"\nПриходите в: {event.place}, будем ждать!",
                            "\nДля связи с организатором пишите в этот чат интересующие вас вопросы,",
                            "либо воспользуйтесь формой в МиниПриложении",
                        ),
                        "chat_id": user.id,
                        "reg_id": registration.id,
                    },
                    eta=eta4,
                )
                await adapter.insert(
                    Notification,
                    {"user_id": user.id, "type": NotificationEnum.INFO, "date_to_valid": eta4, "content": "lol"},
                )
    await adapter.update_by_id(Event, event_id, {"registred": event.registred + 1})
    return okresponse(str(registration.id))
