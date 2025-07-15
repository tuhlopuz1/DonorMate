import logging
from uuid import UUID

from app.dependencies.token_manager import TokenManager
from app.models.db_adapter import adapter
from app.models.db_tables import Registration, User
from fastapi import Security
from fastapi.security import HTTPBearer

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


async def check_qr_data(qr_token: str = Security(Bear)):
    if not qr_token or not qr_token.credentials:
        logger.error("No token")
        return False

    data = TokenManager.decode_qr_token(qr_token.credentials)

    if not data:
        logger.error("No token data")
        return False

    if not data.get("sub") or not data.get("type") or not data.get("iss"):
        logger.error("Invalid token data")
        return False

    if data["type"] != "qr":
        logger.error("Invalid token type")
        return False

    user = await adapter.get_by_id(User, int(data["iss"]))
    registration = await adapter.get_by_id(Registration, UUID(data["sub"]))
    if not user:
        return False
    if registration:
        return user

    logger.info("No registration found fro this token")
    return False
