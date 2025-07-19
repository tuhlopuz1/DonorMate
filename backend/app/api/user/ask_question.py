from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Question, User
from app.models.schemas import QuestionPayload
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/ask-question")
async def ask_question(user: Annotated[User, Depends(check_user_token)], question: QuestionPayload):
    if not user:
        return badresponse("Unauthorized", 401)
    payload = {
        "user_id": user.id,
        "question": question.question,
    }
    question = await adapter.insert(Question, payload)
    return okresponse(str(question.id))
