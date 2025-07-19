from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information, User
from app.models.schemas import Role, UpdateInfoPayload
from fastapi import APIRouter, Depends

router = APIRouter()


@router.put("/edit-user-profile/{num}")
async def edit_user_profile(user: Annotated[User, Depends(check_user_token)], num: int, updates: UpdateInfoPayload):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    user_upd = await adapter.get_by_value(Information, "phone", num)
    if not user_upd:
        return badresponse("User not found", 404)
    user_upd = user_upd[0]
    updates = UpdateInfoPayload.model_dump(updates)
    await adapter.update_by_id(Information, user_upd.id, updates=updates)
    return okresponse()
