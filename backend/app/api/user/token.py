from app.core.config import BOT_TOKEN
from app.dependencies.responses import badresponse
from app.dependencies.telegram import validate_init_data
from app.dependencies.token_manager import TokenManager
from app.models.db_adapter import adapter
from app.models.db_tables import User
from app.models.schemas import TokensResponse
from fastapi import APIRouter, Form

router = APIRouter()


@router.post("/get-token", response_model=TokensResponse)
async def telegram_auth(initData: str = Form(...)):
    print(">>> initData:", initData)
    user_id = validate_init_data(initData, BOT_TOKEN)
    if not user_id:
        return badresponse("Invalid initdata", 403)
    user = await adapter.get_by_id(User, user_id)
    if not user:
        return badresponse("User not found", 404)
    access_token = TokenManager.create_token(
        data={
            "sub": str(user_id),
        },
    )
    refresh_token = TokenManager.create_token(
        {
            "sub": str(user_id),
        },
        access=False,
    )
    return TokensResponse(access=access_token, refresh=refresh_token, role=user.role)
