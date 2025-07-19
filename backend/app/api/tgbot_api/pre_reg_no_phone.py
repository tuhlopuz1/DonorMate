from app.dependencies.responses import okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import User
from fastapi import APIRouter

router = APIRouter()


@router.post("/pre_reg_no_phone")
async def pre_reg_no_phone(id: int):
    await adapter.insert(User, {"id": id})
    return okresponse(code=201)
