from app.dependencies.responses import badresponse, okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import User
from app.models.schemas import TelegramUserInfoPayload
from fastapi import APIRouter

router = APIRouter()


@router.post("/telegram-register")
async def register_telegram_user(user: TelegramUserInfoPayload):
    existing_user = await adapter.get_by_id(User, user.user_id)
    if existing_user:
        return okresponse()
    if not user.username and not user.tg_name:
        return badresponse()
    new_user = {"id": user.user_id, "username": user.username, "telegram_name": user.tg_name}
    await adapter.insert(User, new_user)
    return okresponse(201)
