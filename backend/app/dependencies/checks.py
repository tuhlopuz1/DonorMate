import logging
from fastapi import Request
from app.dependencies.token_manager import TokenManager
from app.models.db_adapter import adapter
from app.models.db_tables import User


logger = logging.getLogger(__name__)


async def check_user_token(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return False
    token = auth.removeprefix("Bearer ").strip()

    data = TokenManager.decode_token(token)
    if not data:
        logger.error("No token data")
        return False

    if not data.get("sub") or not data.get("type"):
        logger.error("Invalid token data")
        return False

    if data["type"] != "access":
        logger.error("Invalid token type")
        return False

    user = await adapter.get_by_id(User, data["sub"])
    if user:
        return user

    logger.error("No user for this token")
    return False
