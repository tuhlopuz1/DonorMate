from typing import Annotated
from uuid import UUID

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, emptyresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Registration, User
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/check-notific/{reg_id}")
async def check_notifications(user: Annotated[User, Depends(check_user_token)], reg_id: UUID):
    if not user:
        return badresponse("Unauthorized", 401)
    reg = await adapter.get_by_id(Registration, reg_id)
    if reg.notification:
        return emptyresponse(200)
    return emptyresponse(204)
