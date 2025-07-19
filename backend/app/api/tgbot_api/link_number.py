from app.dependencies.responses import okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information, User
from fastapi import APIRouter

router = APIRouter()


@router.post("/link-number")
async def link_number(num: int, id: int):
    await adapter.insert(User, {"id": id, "phone": num})
    await adapter.update_by_value(Information, {"phone": num}, {"id": id})
    return okresponse(code=201)
