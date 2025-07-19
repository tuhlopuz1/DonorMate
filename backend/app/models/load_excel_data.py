import logging
import re
from datetime import datetime, timedelta
from io import BytesIO
from typing import Dict, List, Optional, Union

import pandas as pd
from app.models.db_adapter import adapter
from app.models.db_tables import Event, Information, MedicalExemption, Registration, User
from app.models.schemas import Place, Role, UserClass
import pytz
from datetime import time

logger = logging.getLogger(__name__)

class BaseDataLoader:
    MOSCOW_TZ = pytz.timezone('Europe/Moscow')
    UTC_TZ = pytz.utc
    PHONE_CLEAN_PATTERN = re.compile(r"[^+\d]")
    DATE_FORMATS = [
        "%d.%m.%Y", "%d-%m-%Y", "%d/%m/%Y", "%Y.%m.%d", 
        "%Y-%m-%d", "%Y/%m/%d", "%d %b %Y", "%d %B %Y", 
        "%b %d, %Y", "%B %d, %Y"
    ]
    
    def __init__(self, excel_file: Union[bytes, BytesIO], sheet_name: str):
        self.excel_file = excel_file
        self.sheet_name = sheet_name
        self.adapter = adapter
        self.events_cache = {}
        self.users_cache = {}
    
    def _read_excel_data(self) -> List[Dict]:
        """Читает данные из Excel-файла"""
        if isinstance(self.excel_file, bytes):
            file_buffer = BytesIO(self.excel_file)
        else:
            file_buffer = self.excel_file

        xl = pd.ExcelFile(file_buffer)
        sheet_names = xl.sheet_names

        if self.sheet_name in sheet_names:
            df = xl.parse(self.sheet_name)
        else:
            possible_sheets = [name for name in sheet_names 
                              if "пользователи" in name.lower() or "доноры" in name.lower()]
            if possible_sheets:
                logger.warning(f"Sheet '{self.sheet_name}' not found. Using '{possible_sheets[0]}'")
                df = xl.parse(possible_sheets[0])
            else:
                logger.warning(f"Sheet '{self.sheet_name}' not found. Using first sheet")
                df = xl.parse(sheet_names[0])
        
        required_columns = ["Телефон", "ФИО"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            error_msg = f"Missing required columns: {', '.join(missing_columns)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        return df.replace({pd.NaT: None}).to_dict("records")

    def _clean_phone(self, phone: Optional[str]) -> Optional[str]:
        """Очищает и нормализует номер телефона"""
        if not phone or pd.isna(phone):
            return None

        cleaned = self.PHONE_CLEAN_PATTERN.sub("", str(phone))

        if cleaned.startswith("8") and len(cleaned) == 11:
            return "7" + cleaned[1:]
        if cleaned.startswith("+7") and len(cleaned) == 12:
            return cleaned[1:]
        if cleaned.startswith("9") and len(cleaned) == 10:
            return "7" + cleaned
            
        return cleaned

    def _parse_date(self, date_val):
        """Парсит дату из различных форматов"""
        if not date_val or pd.isna(date_val):
            return None
            
        if isinstance(date_val, datetime):
            return date_val
            
        if isinstance(date_val, str):
            date_str = date_val.strip()
            for fmt in self.DATE_FORMATS:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
                    
        try:
            return datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(date_val) - 2)
        except (ValueError, TypeError):
            return None
            
    def _normalize_place(self, place: Optional[str]) -> Optional[Place]:
        """Нормализует название центра крови"""
        if not place:
            return None
        place_str = str(place).strip().lower()
        if "гаврилов" in place_str:
            return Place.GAUR
        elif "фмба" in place_str:
            return Place.FMBA
        return None
            
    def _normalize_user_class(self, user_type: Optional[str]) -> UserClass:
        """Нормализует тип пользователя"""
        if not user_type:
            return UserClass.EXT
        user_type_str = str(user_type).strip().lower()
        if "студент" in user_type_str:
            return UserClass.STU
        if "сотрудник" in user_type_str:
            return UserClass.STF
        return UserClass.EXT

    def _safe_int(self, value) -> int:
        try:
            return int(value) if value and not pd.isna(value) else 0
        except (ValueError, TypeError):
            return 0

class UserLoader(BaseDataLoader):
    """Загрузчик данных о пользователях"""
    def __init__(self, excel_file: Union[bytes, BytesIO], sheet_name: str = "Пользователи"):
        super().__init__(excel_file, sheet_name)
        self.stats = {
            "users_created": 0,
            "users_updated": 0,
            "errors": 0
        }
    
    async def load_data(self) -> Dict:
        """Загружает данные о пользователях из Excel"""
        data = self._read_excel_data()
        for row in data:
            try:
                await self._process_row(row)
            except Exception as e:
                logger.error(f"Error processing row: {e}")
                self.stats["errors"] += 1
        return self.stats

    async def _process_row(self, row: Dict):
        phone = self._clean_phone(row.get("Телефон"))
        if not phone:
            self.stats["errors"] += 1
            return
            
        user = await self._find_or_create_user(phone, row)
        await self._update_user_info(user, row)

    async def _find_or_create_user(self, phone: str, row: Dict) -> User:
        """Находит или создает пользователя по номеру телефона"""
        users = await self.adapter.get_by_value(User, "phone", int(phone))
        if users:
            user = users[0]
            self.stats["users_updated"] += 1
            return user
        
        user_data = {
            "phone": int(phone),
            "role": Role.DONOR,
            "created_at": datetime.now(),
            "notifications_bool": True
        }
        user = await self.adapter.insert(User, user_data)
        self.stats["users_created"] += 1
        logger.info(f"Created new user: {user.id} ({phone})")
        return user

    async def _update_user_info(self, user: User, row: Dict):
        """Обновляет информацию о пользователе"""
        def parse_and_convert(date_val):
            dt = self._parse_date(date_val)
            return dt.replace(tzinfo=None) if dt else None

        last_don_gaur = parse_and_convert(row.get("Дата последней донации Гаврилова"))
        last_don_fmba = parse_and_convert(row.get("Дата последней донации ФМБА"))
        
        user_type_val = row.get("Группа")
        user_class = self._normalize_user_class(user_type_val)
        
        fsp_val = row.get("ФИО")
        fsp = str(fsp_val).strip() if fsp_val is not None else f"Донор {user.phone}"
        if not fsp:
            fsp = f"Донор {user.phone}"
            
        info_data = {
            "id": user.id,
            "phone": user.phone,
            "fsp": fsp,
            "group": str(row.get("Группа", "")).strip(),
            "social": str(row.get("Контакты соцсети", "")).strip(),
            "user_class": user_class,
            "donations_gaur": self._safe_int(row.get("Кол-во Гаврилова", 0)),
            "donations_fmba": self._safe_int(row.get("Кол-во ФМБА", 0)),
            "donations_total": self._safe_int(row.get("Сумма", 0)),
            "last_don_gaur": last_don_gaur,
            "last_don_fmba": last_don_fmba,
        }
        
        existing_info = await self.adapter.get_by_id(Information, user.phone)
        if existing_info:
            await self.adapter.update_by_id(Information, user.phone, info_data)
        else:
            await self.adapter.insert(Information, info_data)
        
        logger.info(f"Updated info for user: {user.id}")

class DonationLoader(BaseDataLoader):
    """Загрузчик данных о донациях"""
    def __init__(self, excel_file: Union[bytes, BytesIO], sheet_name: str = "Донации"):
        super().__init__(excel_file, sheet_name)
        self.stats = {
            "users_created": 0,
            "users_updated": 0,
            "donations_added": 0,
            "events_created": 0,
            "registrations_added": 0
        }
    
    async def load_data(self) -> Dict:
        data = self._read_excel_data()
        for row in data:
            try:
                await self._process_row(row)
            except Exception as e:
                logger.error(f"Error processing row: {e}")
                self.stats["errors"] += 1
        return self.stats

    async def _process_row(self, row: Dict):
        phone = self._clean_phone(row.get("Телефон"))
        if not phone:
            return
            
        user = await self._find_or_create_user(phone, row)
        await self._process_donation(user, row)
        await self._process_registration(user, row)
        await self._process_medical_exemption(user, row)
        await self._process_bm_registration(user, row)

    async def _find_or_create_user(self, phone: str, row: Dict) -> User:
        users = await self.adapter.get_by_value(User, "phone", int(phone))
        if users:
            user = users[0]
            self.stats["users_updated"] += 1
            return user
        
        user_data = {
            "phone": int(phone),
            "role": Role.DONOR,
            "created_at": datetime.now(),
            "notifications_bool": True
        }
        user = await self.adapter.insert(User, user_data)
        self.stats["users_created"] += 1
        
        fsp_val = row.get("ФИО")
        fsp = str(fsp_val).strip() if fsp_val is not None else f"Донор {phone}"
        if not fsp:
            fsp = f"Донор {phone}"
            
        info_data = {
            "id": user.id,
            "phone": user.phone,
            "fsp": fsp,
            "group": str(row.get("Группа", "")).strip(),
            "social": str(row.get("Соцсети", "")).strip(),
            "user_class": self._normalize_user_class(row.get("Тип донора", "Внешний")),
            "donations_gaur": 0,
            "donations_fmba": 0
        }
        await self.adapter.insert(Information, info_data)
        return user

    async def _process_donation(self, user: User, row: Dict):
        donation_place = self._normalize_place(row.get("Место донации", ""))
        donation_date = self._parse_date(row.get("Время донации"))
        
        if donation_date:
            donation_date = donation_date.replace(tzinfo=None)
        
        if not donation_place or not donation_date:
            return
            
        info = await self.adapter.get_by_id(Information, user.phone)
        if not info:
            return
            
        update_data = {}
        
        if donation_place == Place.GAUR:
            update_data["donations_gaur"] = (info.donations_gaur or 0) + 1
            if not info.last_don_gaur or donation_date > info.last_don_gaur:
                update_data["last_don_gaur"] = donation_date
        elif donation_place == Place.FMBA:
            update_data["donations_fmba"] = (info.donations_fmba or 0) + 1
            if not info.last_don_fmba or donation_date > info.last_don_fmba:
                update_data["last_don_fmba"] = donation_date
        
        if update_data:
            update_data["donations_total"] = (info.donations_gaur or 0) + (info.donations_fmba or 0) + 1
            await self.adapter.update_by_id(Information, user.phone, update_data)
            self.stats["donations_added"] += 1

    async def _process_registration(self, user: User, row: Dict):
        event_date = self._parse_date(row.get("Дата акции"))
        place = self._normalize_place(row.get("Центр крови"))
        
        if not event_date or not place:
            return
            
        event = await self._find_or_create_event(event_date, place)
        
        registrations = await self.adapter.get_by_values(Registration, {
            "user_id": user.id,
            "event_id": event.id
        })
        
        if not registrations:
            registration_data = {
                "user_id": user.id,
                "event_id": event.id,
                "accepted": True,
                "closed": True,
                "blood_donated": True
            }
            await self.adapter.insert(Registration, registration_data)
            self.stats["registrations_added"] += 1
            
            await self.adapter.update_by_id(
                Event, 
                event.id, 
                {"registred": event.registred + 1}
            )

    async def _find_or_create_event(self, event_date: datetime, place: Place) -> Event:
        event_date = event_date.astimezone(self.MOSCOW_TZ)
        
        start_date = self.MOSCOW_TZ.localize(
            datetime.combine(event_date.date(), time(10, 0))
        ).astimezone(self.UTC_TZ)
        
        end_date = self.MOSCOW_TZ.localize(
            datetime.combine(event_date.date(), time(18, 0))
        ).astimezone(self.UTC_TZ)
        
        cache_key = f"{start_date.date()}_{place.value}"
        if cache_key in self.events_cache:
            return self.events_cache[cache_key]
        
        events = await self.adapter.get_by_values(Event, {
            "start_date": start_date,
            "place": place
        })
        
        if events:
            event = events[0]
            self.events_cache[cache_key] = event
            return event
        
        event_data = {
            "name": f"День донора {event_date.strftime('%d.%m.%Y')}",
            "place": place,
            "description": f"День донора в {place.value}",
            "start_date": start_date,
            "end_date": end_date,
            "registred": 0
        }
        event = await self.adapter.insert(Event, event_data)
        self.events_cache[cache_key] = event
        self.stats["events_created"] += 1
        return event

    async def _process_medical_exemption(self, user: User, row: Dict):
        start_date = self._parse_date(row.get("Начало отвода"))
        end_date = self._parse_date(row.get("Конец отвода"))
        
        if not start_date:
            return
            
        exemptions = await self.adapter.get_by_value(MedicalExemption, "user_id", user.id)
        if not exemptions:
            exemption_data = {
                "user_id": user.id,
                "start_date": start_date,
                "end_date": end_date,
                "medic_phone_num": str(row.get("Телефон врача", "")).strip(),
                "comment": str(row.get("Причина отвода", "")).strip(),
                "url": str(row.get("Ссылка на документ", "")).strip()
            }
            await self.adapter.insert(MedicalExemption, exemption_data)

    async def _process_bm_registration(self, user: User, row: Dict):
        bm_registered = row.get("Сдал пробирку ДКМ", "").strip().lower() in ["да", "1", "true", "yes"]
        if bm_registered:
            await self.adapter.update_by_id(
                Information, 
                user.phone, 
                {
                    "bm_registered": True,
                    "bm_registration_date": datetime.now().replace(tzinfo=None)
                }
            )

class AdminDataLoader:
    """Управление загрузчиками данных для администратора"""
    @staticmethod
    async def load_donations(excel_file: bytes) -> Dict:
        loader = DonationLoader(excel_file)
        stats = await loader.load_data()
        return {
            "status": "success",
            "message": "Данные о донации успешно загружены",
            "stats": stats
        }
    
    @staticmethod
    async def load_users(excel_file: bytes) -> Dict:
        loader = UserLoader(excel_file, sheet_name="Пользователи")
        stats = await loader.load_data()
        return {
            "status": "success",
            "message": "Данные о пользователях успешно загружены",
            "stats": stats
        }