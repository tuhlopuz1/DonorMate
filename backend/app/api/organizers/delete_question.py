from typing import Annotated
from uuid import UUID

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Question, User
from app.models.schemas import Role
from fastapi import APIRouter, Depends

router = APIRouter()


@router.delete("/delete-question/{question_id}")
async def delete_question(
    user: Annotated[User, Depends(check_user_token)],
    question_id: UUID,
):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    await adapter.delete(Question, question_id)
    return okresponse("Question deleted")
