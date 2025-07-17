from datetime import datetime, timezone
from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import User
from app.models.schemas import ProfileResponse, Role
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from app.models.csv_converter import CSVConverter

router = APIRouter()

@router.get("/get-users-csv")
async def get_users_csv(user: Annotated[User, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    all_users = await adapter.get_all(User)
    users_data = [
        {"id": user.id, "username": user.username, "role": str(user.role).split(".")[1], "created_at": user.created_at, "telegram_name": user.telegram_name, "notifications_bool": user.notifications_bool}
        for user in all_users
    ]
    csv_converter = CSVConverter()
    csv_file_path = await csv_converter.convert(users_data)
    return FileResponse(csv_file_path, media_type="text/csv", filename="users.csv",status_code=200)