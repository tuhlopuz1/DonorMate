from datetime import datetime
from fastapi import APIRouter
from app.api.events.tasks import schedule_telegram_message
from app.dependencies.responses import okresponse

router = APIRouter()


@router.post("/schedule-message")
async def schedule_message(text: str, chat_id: int, eta: datetime):
    schedule_telegram_message.apply_async(
        kwargs={"text": text, "chat_id": chat_id, },
        eta=eta,
    )
    return okresponse()
