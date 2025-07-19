from typing import Annotated
from fastapi import APIRouter, Depends, File, UploadFile
from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.models.db_tables import User
from app.models.schemas import Role
from app.models.load_excel_data import AdminDataLoader

router = APIRouter()

@router.post("/load-donations-xlsx")
async def load_donations_xlsx(
    user: Annotated[User, Depends(check_user_token)], 
    file: UploadFile = File(...)
):
    """Загружает данные о донациях"""
    try:
        if not user or user.role != Role.ADMIN:
            return badresponse("Доступ запрещен", 403)
        
        # Проверка типа файла
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            return badresponse("Недопустимый формат файла. Только Excel", 400)
        
        # Чтение файла
        file_bytes = await file.read()
        result = await AdminDataLoader.load_donations(file_bytes)
        
        return okresponse(result)
    except ValueError as e:
        return badresponse(str(e), 400)
    except Exception as e:
        return badresponse(f"Ошибка обработки файла: {str(e)}", 500)
    finally:
        await file.close()

@router.post("/load-users-xlsx")
async def load_users_xlsx(
    user: Annotated[User, Depends(check_user_token)], 
    file: UploadFile = File(...)
):
    """Загружает данные о пользователях"""
    try:
        if not user or user.role != Role.ADMIN:
            return badresponse("Доступ запрещен", 403)
        
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            return badresponse("Недопустимый формат файла. Только Excel", 400)
        
        file_bytes = await file.read()
        result = await AdminDataLoader.load_users(file_bytes)
        
        return okresponse(result)
    except Exception as e:
        return badresponse(str(e), 400)
    finally:
        await file.close()
