from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import User
from app.models.pdf_reports import generate_organizer_report
from app.models.schemas import Role
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/get-deep-analytics", response_class=FileResponse)
async def get_deep_analytics(
    user: Annotated[User, Depends(check_user_token)],
):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("You are not an admin", 403)
    file_path = await generate_organizer_report(adapter, int(user.id))
    return FileResponse(file_path, media_type="application/pdf", filename="analytics.pdf", status_code=200)
