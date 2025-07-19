from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information, User
from app.models.schemas import PostRegisterPayload
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/post-register")
async def post_registration(user: Annotated[User, Depends(check_user_token)], user_info: PostRegisterPayload):
    if not user:
        return badresponse("Unauthorized", 401)
    updates = user_info.model_dump()
    existing_info = await adapter.get_by_value(Information, "phone", user.id)
    if existing_info:
        await adapter.update_by_id(Information, user.id, updates=updates)
    else:
        updates["id"] = user.id
        await adapter.insert(Information, updates)
    return okresponse()
