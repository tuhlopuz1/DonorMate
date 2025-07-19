from typing import Annotated
from uuid import UUID

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Question, User
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/get-question-by-id")
async def ask_question(user: Annotated[User, Depends(check_user_token)], question_id: UUID):
    if not user:
        return badresponse("Unauthorized", 401)
    question = await adapter.get_by_value(Question, "id", question_id)
    if not question:
        return badresponse("Question not found", 404)
    if question.user_id != user.id:
        return badresponse("You can not get this question", 403)
    return question
