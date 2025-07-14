import hmac
import json
from hashlib import sha256
from urllib.parse import parse_qsl, unquote_plus

from app.core.config import BOT_TOKEN
from app.dependencies.responses import badresponse
from app.dependencies.token_manager import TokenManager
from app.models.db_adapter import adapter
from app.models.db_tables import User
from app.models.schemas import TokensResponse
from fastapi import APIRouter, Request

router = APIRouter()


def verify_init_data(init_data: str) -> dict | None:
    parsed_list = parse_qsl(init_data, keep_blank_values=True)
    parsed = {}
    check_items = []
    hash_ = None

    for k, v in parsed_list:
        if k == "hash":
            hash_ = v
        elif k == "signature":
            continue
        else:
            parsed[k] = v
            check_items.append((k, v))

    if not hash_:
        return None

    check_string = "\n".join(f"{k}={v}" for k, v in sorted(check_items))
    secret_key = sha256(BOT_TOKEN.encode()).digest()
    calc_hash = hmac.new(secret_key, check_string.encode(), sha256).hexdigest()

    if calc_hash != hash_:
        return None

    return parsed


@router.post("/get-token", response_model=TokensResponse, status_code=201)
async def get_token(request: Request):
    init_data_bytes = await request.body()
    init_data = init_data_bytes.decode()

    parsed = verify_init_data(init_data)
    if not parsed:
        return badresponse("Invalid init data", 403)

    try:
        user = json.loads(unquote_plus(parsed["user"]))
        user_id = int(user["id"])
    except Exception:
        return badresponse("Invalid user data", 400)

    user_obj = await adapter.get_by_id(User, user_id)
    if not user_obj:
        return badresponse("User not registered", 404)

    access_token = TokenManager.create_token(data={"sub": str(user_id)})
    refresh_token = TokenManager.create_token(data={"sub": str(user_id)}, access=False)

    return TokensResponse(access=access_token, refresh=refresh_token)
