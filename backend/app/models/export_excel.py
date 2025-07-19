import logging
import pandas as pd
from io import BytesIO
from app.models.db_adapter import adapter
from app.models.db_tables import User, Information
from app.models.schemas import UserClass
from sqlalchemy import select
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)

class UserExporter:
    """Класс для экспорта данных пользователей в Excel"""
    COLUMN_MAPPING = {
        "phone": "Телефон",
        "fsp": "ФИО",
        "group": "Группа",
        "social": "Контакты соцсети",
        "user_class": "Тип пользователя",
        "donations_gaur": "Кол-во Гаврилова",
        "donations_fmba": "Кол-во ФМБА",
        "last_don_gaur": "Дата последней донации Гаврилова",
        "last_don_fmba": "Дата последней донации ФМБА"
    }
    
    USER_CLASS_MAPPING = {
        UserClass.STU: "Студент",
        UserClass.STF: "Сотрудник",
        UserClass.EXT: "Внешний"
    }

    @classmethod
    async def export_users(cls) -> BytesIO:
        """Экспортирует всех пользователей в Excel-файл"""
        logger.info("Starting user data export")
        
        try:
            # Создаем новую сессию
            async with adapter.SessionLocal() as session:
                # Получаем всех пользователей с информацией
                stmt = select(User).options(selectinload(User.info))
                result = await session.execute(stmt)
                users = result.scalars().all()
                
                if not users:
                    logger.warning("No users found for export")
                    return BytesIO()
                
                # Собираем данные для экспорта
                data = []
                for user in users:
                    row = {
                        "phone": user.phone,
                        "fsp": user.info.fsp if user.info else "",
                        "group": user.info.group if user.info else "",
                        "social": user.info.social if user.info else "",
                        "user_class": cls.USER_CLASS_MAPPING.get(
                            user.info.user_class if user.info else UserClass.EXT, 
                            "Неизвестно"
                        ),
                        "donations_gaur": user.info.donations_gaur if user.info else 0,
                        "donations_fmba": user.info.donations_fmba if user.info else 0,
                        "last_don_gaur": cls._format_date(user.info.last_don_gaur if user.info else None),
                        "last_don_fmba": cls._format_date(user.info.last_don_fmba if user.info else None)
                    }
                    data.append(row)
                
                # Создаем DataFrame
                df = pd.DataFrame(data)
                
                # Переименовываем колонки
                df.rename(columns=cls.COLUMN_MAPPING, inplace=True)
                
                # Создаем Excel-файл в памяти
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Пользователи', index=False)
                    
                    # Автонастройка ширины колонок
                    if not df.empty:
                        worksheet = writer.sheets['Пользователи']
                        for idx, col in enumerate(df.columns):
                            max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                            worksheet.column_dimensions[chr(65 + idx)].width = min(max_len, 50)
                
                output.seek(0)
                logger.info(f"Successfully exported {len(users)} users to Excel")
                return output
                
        except Exception as e:
            logger.error(f"Error exporting users: {str(e)}", exc_info=True)
            # Возвращаем пустой файл с ошибкой в логах
            output = BytesIO()
            df = pd.DataFrame({"Error": [str(e)]})
            df.to_excel(output, sheet_name='Ошибка', index=False)
            output.seek(0)
            return output

    @staticmethod
    def _format_date(date_val):
        """Форматирует дату в строку"""
        if date_val:
            return date_val.strftime("%d.%m.%Y")
        return ""