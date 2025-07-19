from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.schemas import Role
from app.models.export_excel import UserExporter
from app.models.db_tables import User

router = APIRouter()

@router.get("/get-users-excel")
async def get_users_excel(user: Annotated[User, Depends(check_user_token)]):
    try:
        if not user:
            return badresponse("Unauthorized", 401)
        if user.role != Role.ADMIN:
            return badresponse("Forbidden", 403)
        
        file = await UserExporter.export_users()
        file.seek(0)
        
        return StreamingResponse(
            file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=users.xlsx"}
        )
    except Exception as e:
        return badresponse(str(e), 400)