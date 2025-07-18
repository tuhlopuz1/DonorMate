from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.models.db_tables import User
from app.models.load_excel_data import DataLoader
from app.models.schemas import Role
from fastapi import APIRouter, Depends, File

router = APIRouter()


@router.post("/load-xlsx")
async def load_xlsx(user: Annotated[User, Depends(check_user_token)], file_bytes: bytes = File(...)):
    try:
        if not user:
            return badresponse("Unauthorized", 401)
        if user.role != Role.ADMIN:
            return badresponse("You can not load excel because you are not an admin", 403)
        await DataLoader(file_bytes).load_data()
        return okresponse("Data loaded successfully")
    except Exception as e:
        return badresponse(str(e), 400)
