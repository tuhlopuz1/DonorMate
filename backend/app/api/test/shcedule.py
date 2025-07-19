from datetime import datetime
from uuid import UUID

from app.api.tasks import schedule_telegram_qr
from app.dependencies.responses import okresponse
from app.dependencies.token_manager import TokenManager
from fastapi import APIRouter

router = APIRouter()


@router.post("/schedule-message")
async def schedule_message(text: str, chat_id: int, reg_id: UUID, eta: datetime):
    qr_data = TokenManager.encode_qr_token({"iss": str(chat_id), "sub": str(reg_id)}, expire_sec=6000)
    schedule_telegram_qr.apply_async(
        kwargs={"text": text, "chat_id": chat_id, "reg_id": reg_id, "data": qr_data},
        eta=eta,
    )
    return okresponse()
