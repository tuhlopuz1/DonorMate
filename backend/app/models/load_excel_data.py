import logging
import re
from datetime import datetime
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

from app.models.schemas import DonorEarlier, Gender
from app.models.db_tables import Gender, Role, User, InfoForExcel
from app.models.db_adapter import adapter, AsyncDatabaseAdapter

logger = logging.getLogger(__name__)


class DataLoader:
    DATE_FORMATS = [
        "%d.%m.%Y", "%d-%m-%Y", "%d/%m/%Y", 
        "%Y.%m.%d", "%Y-%m-%d", "%Y/%m/%d",
        "%d %b %Y", "%d %B %Y", "%b %d, %Y", "%B %d, %Y"
    ]
    PHONE_CLEAN_PATTERN = re.compile(r"[^+\d]")

    def __init__(
        self, 
        excel_file: Union[bytes, BytesIO], 
        sheet_name: str = "Полная БД",
        adapter: AsyncDatabaseAdapter = adapter
    ):
        self.excel_file = excel_file
        self.sheet_name = sheet_name
        self.adapter = adapter

    async def load_data(self) -> None:
        """Основной метод для загрузки данных из Excel в БД"""
        data = self._read_excel_data()
        for row in data:
            try:
                user_data, info_data = self._parse_row(row)
                await self._insert_user_data(user_data, info_data)
            except Exception as e:
                logger.error(f"Error processing row {row}: {str(e)}")

    def _read_excel_data(self) -> List[Dict]:
        """Чтение данных из Excel файла (из байтов или BytesIO)"""
        if isinstance(self.excel_file, bytes):
            file_buffer = BytesIO(self.excel_file)
        else:
            file_buffer = self.excel_file
            
        df = pd.read_excel(file_buffer, sheet_name=self.sheet_name)
        return df.replace({pd.NaT: None}).to_dict("records")

    def _parse_row(self, row: Dict) -> Tuple[Dict, Dict]:
        """Разбор строки данных на составляющие для User и InfoForExcel"""
        # Обработка ФИО с улучшенной логикой
        fullname = str(row.get("ФИО", "")).strip()
        name_parts = fullname.split()
        
        # Обработка разных случаев количества слов в ФИО
        if len(name_parts) == 0:
            surname = "Неизвестно"
            name = "Неизвестно"
            patronymic = None
        elif len(name_parts) == 1:
            surname = name_parts[0]
            name = "Неизвестно"
            patronymic = None
        elif len(name_parts) == 2:
            surname = name_parts[0]
            name = name_parts[1]
            patronymic = None
        else:
            surname = name_parts[0]
            name = name_parts[1]
            patronymic = " ".join(name_parts[2:])

        # Определение роли
        group = str(row.get("Группа", "")).strip()
        role = Role.ADMIN if self._is_staff(group) else Role.DONOR

        # Обработка дат
        last_donation_gavrilov = self._parse_date(row.get("Дата последней донации Гаврилова"))
        last_donation_fmba = self._parse_date(row.get("Дата последней донации ФМБА"))

        # Обработка числовых значений
        donations_gavrilov = self._safe_int(row.get("Кол-во Гаврилова"))
        donations_fmba = self._safe_int(row.get("Кол-во ФМБА"))
        total_donations = self._safe_int(row.get("Сумма"))

        # Подготовка данных для User
        user_data = {
            "role": role,
            "notifications_bool": True
        }

        # Подготовка данных для InfoForExcel
        info_data = {
            "surname": surname,
            "name": name,
            "patronymic": patronymic,
            "fullname": fullname,
            "group": group,
            "donations_gavrilov": donations_gavrilov,
            "donations_fmba": donations_fmba,
            "last_donation_gavrilov": last_donation_gavrilov,
            "last_donation_fmba": last_donation_fmba,
            "social_media": str(row.get("Контакты соцсети", "")).strip() or None,
            "phone": self._clean_phone(row.get("Телефон")),
            "gender": Gender.UNDEFINED,
            "birth_date": None,
            "university": None,
            "weight": 0,
            "chronic_disease": False,
            "medical_exemption": False,
            "donor_earlier": DonorEarlier.YES,
            "feedback": None,
            "donations": total_donations
        }

        return user_data, info_data

    def _is_staff(self, group: Optional[str]) -> bool:
        """Определяет, является ли пользователь сотрудником"""
        return group and "сотрудник" in group.lower()

    def _safe_int(self, value) -> int:
        """Безопасное преобразование в int"""
        try:
            return int(value) if value and not pd.isna(value) else 0
        except (ValueError, TypeError):
            return 0

    def _parse_date(self, date_val):
        """Парсинг даты из различных форматов"""
        if not date_val or pd.isna(date_val):
            return None
        
        # Если значение уже является датой
        if isinstance(date_val, datetime):
            return date_val.date()
        
        # Обработка строковых значений
        if isinstance(date_val, str):
            # Удаление лишних пробелов
            date_str = date_val.strip()
            
            # Обработка периодов (например "2014-2019")
            if "-" in date_str and len(date_str) > 7:
                return None
                
            # Обработка года без даты
            if len(date_str) == 4 and date_str.isdigit():
                return datetime(int(date_str), 1, 1).date()
            
            # Стандартизация разделителей
            date_str = date_str.replace('/', '.').replace('-', '.')
            
            # Попробуем все форматы
            for fmt in self.DATE_FORMATS:
                try:
                    return datetime.strptime(date_str, fmt).date()
                except ValueError:
                    continue
        
        # Попробуем преобразовать из числа Excel
        try:
            return datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(date_val) - 2).date()
        except (ValueError, TypeError):
            return None

    def _clean_phone(self, phone: Optional[str]) -> Optional[str]:
        """Очистка номера телефона от лишних символов"""
        if not phone or pd.isna(phone):
            return None
            
        # Приведение к строке и удаление всех нецифровых символов кроме +
        cleaned = self.PHONE_CLEAN_PATTERN.sub("", str(phone))
        
        # Нормализация российских номеров
        if cleaned.startswith('8') and len(cleaned) == 11:
            return '+7' + cleaned[1:]
        elif cleaned.startswith('7') and len(cleaned) == 11:
            return '+7' + cleaned[1:]
        elif len(cleaned) == 10:
            return '+7' + cleaned
            
        return cleaned

    async def _insert_user_data(self, user_data: Dict, info_data: Dict) -> None:
        """Вставка данных пользователя в БД"""
        async with self.adapter.SessionLocal() as session:
            try:
                # Создание пользователя
                user = User(**user_data)
                session.add(user)
                await session.flush()  # Для получения ID пользователя
                
                # Создание информации о пользователе
                info_data["id"] = user.id
                info = InfoForExcel(**info_data)
                session.add(info)
                
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error: {str(e)}")
                raise