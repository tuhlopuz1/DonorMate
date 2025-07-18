from app.dependencies.responses import emptyresponse
from app.models.db_adapter import adapter
from app.models.db_tables import User
from fastapi import APIRouter

router = APIRouter()


@router.get("/is-registred/{id}")
async def is_user_registred(id: int):
    user = await adapter.get_by_id(User, id)
    if user:
        return emptyresponse(code=200)
    return emptyresponse(code=204)
