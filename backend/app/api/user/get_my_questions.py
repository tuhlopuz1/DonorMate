from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Questions, User
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/get-my-questions")
async def ask_question(user: Annotated[User, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    user_questions = await adapter.get_by_value(Questions, "user_id", user.id)
    return user_questions
