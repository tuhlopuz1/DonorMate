from app.dependencies.responses import emptyresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information
from fastapi import APIRouter

router = APIRouter()


@router.get("/is-registred/{id}")
async def is_user_registred(id: int):
    info = await adapter.get_by_id(Information, id)
    if info:
        return emptyresponse(code=200)
    return emptyresponse(code=204)
