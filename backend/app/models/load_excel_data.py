import logging
import re
from datetime import datetime
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Union
from app.models.db_tables import *
import pandas as pd
from app.models.db_adapter import adapter
from app.models.db_tables import Information

logger = logging.getLogger(__name__)


class DataLoader:
    DATE_FORMATS = [
        "%d.%m.%Y",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y.%m.%d",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d %b %Y",
        "%d %B %Y",
        "%b %d, %Y",
        "%B %d, %Y",
    ]
    PHONE_CLEAN_PATTERN = re.compile(r"[^+\d]")

    def __init__(
        self,
        excel_file: Union[bytes, BytesIO],
        sheet_name: str = "Полная БД",
    ):
        self.excel_file = excel_file
        self.sheet_name = sheet_name
        self.adapter = adapter

    async def load_data(self) -> None:
        data = self._read_excel_data()
        for row in data:
            try:
                info_data = self._parse_row(row)
                await adapter.insert(Information, info_data)
            except Exception as e:
                logger.error(f"Error processing row {row}: {str(e)}")

    def _read_excel_data(self) -> List[Dict]:
        if isinstance(self.excel_file, bytes):  
            file_buffer = BytesIO(self.excel_file)
        else:
            file_buffer = self.excel_file

        df = pd.read_excel(file_buffer, sheet_name=self.sheet_name)
        return df.replace({pd.NaT: None}).to_dict("records")

    def _parse_row(self, row: Dict) -> Tuple[Dict, Dict]:
        fsp = str(row.get("ФИО", "")).strip()
        phone = str(row.get("Телефон", "")).strip()
        group = str(row.get("Группа", "")).strip()
        social = str(row.get("Контакты соцсети", "")).strip()
        last_don_gaur = self._parse_date(row.get("Дата последней донации Гаврилова"))
        last_don_fmba = self._parse_date(row.get("Дата последней донации ФМБА"))
        donations_gaur = self._safe_int(row.get("Кол-во Гаврилова"))
        donations_fmba = self._safe_int(row.get("Кол-во ФМБА"))

        info_data = {
            "phone": phone,
            "fsp": fsp,
            "group": group,
            "social": social,
            "donations_gaur": donations_gaur,
            "donations_fmba": donations_fmba,
            "last_don_gaur": last_don_gaur,
            "last_don_fmba": last_don_fmba,
        }

        return info_data

    def _safe_int(self, value) -> int:
        try:
            return int(value) if value and not pd.isna(value) else 0
        except (ValueError, TypeError):
            return 0

    def _parse_date(self, date_val):
        if not date_val or pd.isna(date_val):
            return None
        if isinstance(date_val, datetime):
            return date_val.date()
        if isinstance(date_val, str):
            date_str = date_val.strip()
            if "-" in date_str and len(date_str) > 7:
                return None
            if len(date_str) == 4 and date_str.isdigit():
                return datetime(int(date_str), 1, 1).date()

            date_str = date_str.replace("/", ".").replace("-", ".")

            for fmt in self.DATE_FORMATS:
                try:
                    return datetime.strptime(date_str, fmt).date()
                except ValueError:
                    continue

        try:
            return datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(date_val) - 2).date()
        except (ValueError, TypeError):
            return None

    def _clean_phone(self, phone: Optional[str]) -> Optional[str]:
        if not phone or pd.isna(phone):
            return None

        cleaned = self.PHONE_CLEAN_PATTERN.sub("", str(phone))

        if len(cleaned) == 11:
            return cleaned[1:]
        return cleaned


# class DonationLoader:
#     PHONE_CLEAN_PATTERN = re.compile(r"[^+\d]")
#     DATE_FORMATS = [
#         "%d.%m.%Y",
#         "%d-%m-%Y",
#         "%d/%m/%Y",
#         "%Y.%m.%d",
#         "%Y-%m-%d",
#         "%Y/%m/%d",
#         "%d %b %Y",
#         "%d %B %Y",
#         "%b %d, %Y",
#         "%B %d, %Y",
#     ]

#     def __init__(self, excel_file: Union[bytes, BytesIO], sheet_name: str = "Донации"):
#         self.excel_file = excel_file
#         self.sheet_name = sheet_name
#         self.adapter = adapter

#     async def load_data(self) -> None:
#         """Загружает данные о донациях из Excel и обновляет информацию в базе"""
#         data = self._read_excel_data()
#         for row in data:
#             try:
#                 phone = self._clean_phone(row.get("Телефон"))
#                 if not phone:
#                     continue
                
#                 # Найти или создать пользователя
#                 user = await self._find_or_create_user(phone)
#                 if not user:
#                     continue
                
#                 # Обработать информацию о донации
#                 await self._process_donation(user, row)
                
#             except Exception as e:
#                 print(f"Error processing row: {e}")

#     def _read_excel_data(self) -> List[Dict]:
#         """Читает данные из Excel-файла"""
#         if isinstance(self.excel_file, bytes):
#             file_buffer = BytesIO(self.excel_file)
#         else:
#             file_buffer = self.excel_file

#         df = pd.read_excel(file_buffer, sheet_name=self.sheet_name)
#         return df.replace({pd.NaT: None}).to_dict("records")

#     async def _find_or_create_user(self, phone: str) -> Optional[User]:
#         """Находит или создает пользователя по номеру телефона"""
#         # Поиск существующего пользователя
#         users = await self.adapter.get_by_value(User, "phone", phone)
#         if users:
#             return users[0]
        
#         # Создание нового пользователя, если не найден
#         user_data = {
#             "phone": phone,
#             "role": Role.DONOR,
#             "created_at": datetime.now(),
#             "notifications_bool": True
#         }
#         return await self.adapter.insert(User, user_data)

#     async def _process_donation(self, user: User, row: Dict):
#         """Обновляет информацию о донациях пользователя"""
#         donation_place = str(row.get("Место донации", "")).strip().lower()
#         donation_date = self._parse_date(row.get("Время донации"))
        
#         if not donation_place or not donation_date:
#             return
            
#         # Получаем или создаем запись информации о пользователе
#         info = await self.adapter.get_by_id(Information, user.phone)
        
#         if info:
#             # Обновляем существующую запись
#             update_data = {}
            
#             if "гаврилов" in donation_place or "гаврилова" in donation_place:
#                 update_data["donations_gaur"] = (info.donations_gaur or 0) + 1
#                 if not info.last_don_gaur or donation_date > info.last_don_gaur:
#                     update_data["last_don_gaur"] = donation_date
            
#             elif "фмба" in donation_place:
#                 update_data["donations_fmba"] = (info.donations_fmba or 0) + 1
#                 if not info.last_don_fmba or donation_date > info.last_don_fmba:
#                     update_data["last_don_fmba"] = donation_date
            
#             if update_data:
#                 await self.adapter.update_by_id(Information, user.phone, update_data)
#         else:
#             # Создаем новую запись
#             info_data = {
#                 "phone": user.phone,
#                 "fsp": f"Донор {user.phone}",
#             }
            
#             if "гаврилов" in donation_place or "гаврилова" in donation_place:
#                 info_data["donations_gaur"] = 1
#                 info_data["last_don_gaur"] = donation_date
#             elif "фмба" in donation_place:
#                 info_data["donations_fmba"] = 1
#                 info_data["last_don_fmba"] = donation_date
            
#             await self.adapter.insert(Information, info_data)

#     def _clean_phone(self, phone: Optional[str]) -> Optional[str]:
#         """Очищает и нормализует номер телефона"""
#         if not phone or pd.isna(phone):
#             return None

#         cleaned = self.PHONE_CLEAN_PATTERN.sub("", str(phone))

#         # Нормализация российских номеров
#         if cleaned.startswith("8") and len(cleaned) == 11:
#             return "7" + cleaned[1:]
#         if cleaned.startswith("+7") and len(cleaned) == 12:
#             return cleaned[1:]
#         if cleaned.startswith("9") and len(cleaned) == 10:
#             return "7" + cleaned
            
#         return cleaned

#     def _parse_date(self, date_val):
#         """Парсит дату из различных форматов"""
#         if not date_val or pd.isna(date_val):
#             return None
            
#         if isinstance(date_val, datetime):
#             return date_val
            
#         if isinstance(date_val, str):
#             date_str = date_val.strip()
#             for fmt in self.DATE_FORMATS:
#                 try:
#                     return datetime.strptime(date_str, fmt)
#                 except ValueError:
#                     continue
                    
#         try:
#             # Попробуем преобразовать как timestamp Excel
#             return datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(date_val) - 2)
#         except (ValueError, TypeError):
#             return None
    