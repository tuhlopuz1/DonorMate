from fastapi import APIRouter
from urllib.parse import parse_qsl
import hmac
from hashlib import sha256
from app.models.schemas import InitDataPayload, TokensResponse
from app.core.config import BOT_TOKEN
from app.dependencies.token_manager import TokenManager
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import User

router = APIRouter()


def verify_init_data(init_data: str) -> dict:
    parsed = dict(parse_qsl(init_data))
    hash_ = parsed.pop("hash", None)
    check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
    secret = sha256(BOT_TOKEN.encode()).digest()
    calc_hash = hmac.new(secret, check_string.encode(), sha256).hexdigest()
    if calc_hash != hash_:
        return False
    return parsed


@router.post("/get-token", response_model=TokensResponse, status_code=201)
async def get_token(payload: InitDataPayload):
    parsed = verify_init_data(payload.InitData)
    if not parsed:
        return badresponse("Invalid init data", 403)
    user_id = int(parsed.get("user", "").split(":")[0])
    if not user_id:
        return badresponse("User not found", 404)
    existing_user = await adapter.get_by_id(User, user_id)
    if not existing_user:
        return badresponse("User not registred", 404)
    access_token = TokenManager.create_token(
        data={
            "sub": user_id
        }
    )
    refresh_token = TokenManager.create_token(
        data={
            "sub": user_id
        },
        access=False,
    )
    return TokensResponse(access=access_token, refresh=refresh_token)
