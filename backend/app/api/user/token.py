import hmac
import json
from hashlib import sha256
from urllib.parse import unquote_plus

from app.core.config import BOT_TOKEN
from app.dependencies.responses import badresponse
from app.dependencies.token_manager import TokenManager
from app.models.db_adapter import adapter
from app.models.db_tables import User
from app.models.schemas import InitDataPayload, TokensResponse
from fastapi import APIRouter

router = APIRouter()


def verify_init_data(init_data: str) -> dict | None:
    # Разбиваем initData на пары key=value
    items = init_data.split("&")
    data_check = []
    hash_value = None

    for item in items:
        if item.startswith("hash="):
            hash_value = item.split("=", 1)[1]
        elif item.startswith("signature="):
            continue  # пропускаем signature
        else:
            data_check.append(item)

    if not hash_value:
        return None

    # Сортируем и объединяем
    check_string = "\n".join(sorted(data_check))

    secret_key = sha256(BOT_TOKEN.encode()).digest()
    calc_hash = hmac.new(secret_key, check_string.encode(), sha256).hexdigest()

    if calc_hash != hash_value:
        return None

    # Преобразуем в словарь (с URL-decoding только ключей)
    parsed = dict(item.split("=", 1) for item in data_check)

    # Декодируем JSON в поле "user"
    if "user" in parsed:
        parsed["user"] = json.loads(unquote_plus(parsed["user"]))

    return parsed


@router.post("/get-token", response_model=TokensResponse, status_code=201)
async def get_token(payload: InitDataPayload):
    parsed = verify_init_data(payload.InitData)
    if not parsed:
        return badresponse("Invalid init data", 403)

    user_data = parsed.get("user")
    if not user_data or "id" not in user_data:
        return badresponse("User not found", 404)

    user_id = int(user_data["id"])

    existing_user = await adapter.get_by_id(User, user_id)
    if not existing_user:
        return badresponse("User not registered", 404)

    access_token = TokenManager.create_token(data={"sub": str(user_id)})
    refresh_token = TokenManager.create_token(data={"sub": str(user_id)}, access=False)

    return TokensResponse(access=access_token, refresh=refresh_token)
