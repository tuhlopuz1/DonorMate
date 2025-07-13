from fastapi import APIRouter

from app.models.db_adapter import adapter
from app.models.db_tables import User
from app.models.schemas import TelegramUserInfoPayload
from app.dependencies.responses import okresponse, emptyresponse

router = APIRouter()


@router.post("/telegram-register")
async def register_telegram_user(user: TelegramUserInfoPayload):
    existing_user = await adapter.get_by_id(User, user.id)
    if existing_user:
        return emptyresponse()
    new_user = {
        "id": user.id,
        "username": user.username,
        "telegram_name": user.tg_name
    }
    adapter.insert(User, new_user)
    return okresponse(code=201)
