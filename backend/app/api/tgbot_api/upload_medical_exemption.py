from datetime import datetime
from typing import Annotated, Optional

from app.core.config import DOCUMENTS_BUCKET
from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import MedicalExemption, User
from app.models.s3_adapter import S3HttpxSigV4Adapter
from app.models.schemas import MedicalExemptionResponse
from fastapi import APIRouter, Depends, File, Form, UploadFile

router = APIRouter()


@router.post("/upload-medical-exemption")
async def upload_medical_exemption(
    user: Annotated[User, Depends(check_user_token)],
    start_date: datetime = Form(...),
    end_date: datetime = Form(...),
    medic_phone_num: Optional[str] = Form(default=None),
    comment: Optional[str] = Form(default=None),
    file: UploadFile = File(...),
):
    if not user:
        return badresponse("Unauthorized", 401)
    med_exemp_dict = {
        "start_date": start_date,
        "end_date": end_date,
        "medic_phone_num": medic_phone_num,
        "comment": comment,
        "user_id": user.id,
    }
    try:
        document = await adapter.insert(MedicalExemption, med_exemp_dict)

        filename = f"{user.id}/{document.id}"
        s3 = S3HttpxSigV4Adapter(DOCUMENTS_BUCKET)
        await s3.upload_file(file, filename)
        url = s3.get_url(filename)
        await adapter.update_by_id(MedicalExemption, document.id, {"url": url})
        return MedicalExemptionResponse(id=document.id, url=url)
    except Exception as e:
        return badresponse(f"Uploading error: {e}", 500)
