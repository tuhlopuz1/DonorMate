import logging
from fastapi import Security
from fastapi.security import HTTPBearer
from app.dependencies.token_manager import TokenManager
from app.models.db_adapter import adapter
from app.models.db_tables import User


logger = logging.getLogger(__name__)

Bear = HTTPBearer(auto_error=False)


async def check_user_token(access_token: str = Security(Bear)):
    if not access_token or not access_token.credentials:
        logger.error("No token")
        return False

    data = TokenManager.decode_token(access_token.credentials)

    if not data:
        logger.error("No token data")
        return False

    if not data.get("sub") or not data.get("type"):
        logger.error("Invalid token data")
        return False

    if data["type"] != "access":
        logger.error("Invalid token type")
        return False

    user = await adapter.get_by_id(User, int(data["sub"]))
    if user:
        return user

    logger.error("No user for this token")
    return False
