from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, emptyresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information, User
from fastapi import APIRouter, Depends

router = APIRouter()


@router.delete("/delete-user")
async def delete_user(user: Annotated[User, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    await adapter.delete(User, user.id)
    await adapter.delete(Information, user.id)
    return emptyresponse()
