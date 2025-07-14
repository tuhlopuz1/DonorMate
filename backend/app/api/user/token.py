from app.core.config import BOT_TOKEN
from app.dependencies.telegram import validate_init_data
from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/auth/telegram")
async def telegram_auth(initData: str = Form(...)):
    """
    Проверяет подпись initData от Telegram WebApp.
    """

    is_valid = validate_init_data(initData, BOT_TOKEN)

    if not is_valid:
        return JSONResponse(
            status_code=403,
            content={"detail": "Invalid initData signature"},
        )

    return {"status": "ok", "message": "initData is valid"}
