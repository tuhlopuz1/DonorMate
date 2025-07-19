from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information, User
from app.models.schemas import UpdateInfoPayload
from fastapi import APIRouter, Depends

router = APIRouter()


@router.put("/update-user-info")
async def update_user_info(user: Annotated[User, Depends(check_user_token)], info: UpdateInfoPayload):
    if not user:
        return badresponse("Unauthorized", 401)
    info_dict = UpdateInfoPayload.model_dump(info)
    if not info_dict:
        return badresponse()
    await adapter.update_by_value(Information, user.phone, info_dict)
    return okresponse()
