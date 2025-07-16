from typing import Annotated

from app.core.config import ADMIN_IDS
from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import User
from app.models.redis_adapter import redis_adapter
from app.models.schemas import Role
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/set-organizer/{code}")
async def set_org_status(user: Annotated[User, Depends(check_user_token)], code: str):
    if not user:
        return badresponse("Unauthorized", 401)
    existing_code = await redis_adapter.get(f"admin_code:{code}")
    if not existing_code or existing_code not in ADMIN_IDS:
        return badresponse("Wrong code", 403)
    await adapter.update_by_id(User, user.id, {"role": Role.ADMIN})
    return okresponse()
