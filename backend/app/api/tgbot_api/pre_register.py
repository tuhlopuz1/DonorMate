from app.dependencies.responses import okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import User
from fastapi import APIRouter

router = APIRouter()


@router.post("/pre-register")
async def pre_register(num: int, id: int):
    await adapter.insert(User, {"id": id, "phone": num})
    return okresponse(code=201)
