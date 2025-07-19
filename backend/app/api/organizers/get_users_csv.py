from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.csv_converter import CSVConverter
from app.models.db_adapter import adapter
from app.models.db_tables import Information, User
from app.models.schemas import ProfileResponse, Role
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/get-users-csv")
async def get_users_csv(user: Annotated[User, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    all_users_data = await adapter.get_all_with_join(User, Information, "id")
    all_users = []
    for userr in all_users_data:
        userr = ProfileResponse.model_validate(userr)
        userr.donations = userr.donations_fmba + userr.donations_gaur
        all_users.append(userr)
    csv_converter = CSVConverter()
    csv_file_path = await csv_converter.convert(all_users)
    return FileResponse(csv_file_path, media_type="text/csv", filename="users.csv", status_code=200)
