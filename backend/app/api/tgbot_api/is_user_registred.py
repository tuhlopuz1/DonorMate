from fastapi import APIRouter
from app.models.db_adapter import adapter
from app.models.db_tables import User, Information
from app.dependencies.responses import okresponse

router = APIRouter()


@router.get("/is-registred/{id}")
async def is_user_registred(id: int):
    user = await adapter.get_by_id(User, id)
    info = await adapter.get_by_id(Information, id)
    if info:
        return okresponse(code=200)
    return okresponse(code=204)
