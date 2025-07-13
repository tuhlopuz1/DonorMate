from datetime import datetime, timedelta, timezone
from fastapi import APIRouter
from app.api.events.tasks import schedule_telegram_message
from app.dependencies.responses import okresponse

router = APIRouter()


@router.post("/schedule-message")
async def schedule_message(text: str, chat_id: int, delay_in_sec: float = 60.0):
    eta = datetime.now(timezone.utc) + timedelta(seconds=delay_in_sec)
    schedule_telegram_message.apply_async(
        kwargs={"text": text, "chat_id": chat_id, },
        eta=eta,
    )
    return okresponse()
