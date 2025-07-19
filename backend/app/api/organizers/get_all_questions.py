from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Questions
from app.models.schemas import ProfileResponse, Role
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/get-all-questions")
async def get_all_questions(user: Annotated[ProfileResponse, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    quetions = await adapter.get_all(Questions)
    return quetions