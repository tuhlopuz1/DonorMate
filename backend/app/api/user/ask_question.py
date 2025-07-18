from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import MedicalExemption, User, Questions
from fastapi import APIRouter, Depends
from app.models.schemas import QAPayload

router = APIRouter()

@router.post("/ask-question")
async def ask_question(user: Annotated[User, Depends(check_user_token)], question: QAPayload):
    if not user:
        return badresponse("Unauthorized", 401)
    if question.answer != None:
        return badresponse("You can not answer your question", 400)
    payload = {
        "user_id": user.id,
        "question": question.question,
        "answer": None,
    }
    await adapter.insert(Questions, payload)
    return okresponse()

    