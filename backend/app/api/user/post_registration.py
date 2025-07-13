from typing import Annotated
from fastapi import APIRouter, Depends
from app.models.schemas import PostRegisterPayload
from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import User

router = APIRouter()


@router.post("/post-register")
async def post_registration(
    user: Annotated[User, Depends(check_user_token)],
    user_info: PostRegisterPayload
):
    if not user:
        return badresponse("Unauthorized", 401)
    updates = {
        "fullname": user_info.fullname,
        "surname": user_info.surname,
        "patronymic": user_info.patronymic,
        "birth_date": user_info.birth_date,
    }
    await adapter.update_by_id(User, user.id, updates=updates)
    return okresponse()
