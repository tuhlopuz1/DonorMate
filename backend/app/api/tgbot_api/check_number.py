from app.dependencies.responses import emptyresponse, okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information
from fastapi import APIRouter

router = APIRouter()


@router.get("/check-num/{num}")
async def check_num(num: int):
    existing_num = await adapter.get_by_value(Information, "phone", num)
    if existing_num:
        return okresponse(existing_num.fsp, 201)
    return emptyresponse(204)
