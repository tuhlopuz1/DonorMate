import logging
import re

# from datetime import datetime
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Union

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
                await adapter.inser(Information, info_data)
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
        # Обработка дат
        # last_donation_gavrilov = self._parse_date(row.get("Дата последней донации Гаврилова"))
        # last_donation_fmba = self._parse_date(row.get("Дата последней донации ФМБА"))
        # Обработка числовых значений
        # donations_gavrilov = self._safe_int(row.get("Кол-во Гаврилова"))
        # donations_fmba = self._safe_int(row.get("Кол-во ФМБА"))
        donations = self._safe_int(row.get("Сумма"))

        info_data = {"phone": phone, "fsp": fsp, "group": group, "donations": donations}

        return info_data

    def _safe_int(self, value) -> int:
        try:
            return int(value) if value and not pd.isna(value) else 0
        except (ValueError, TypeError):
            return 0

    # def _parse_date(self, date_val):
    #     if not date_val or pd.isna(date_val):
    #         return None
    #     if isinstance(date_val, datetime):
    #         return date_val.date()
    #     if isinstance(date_val, str):
    #         date_str = date_val.strip()
    #         if "-" in date_str and len(date_str) > 7:
    #             return None
    #         if len(date_str) == 4 and date_str.isdigit():
    #             return datetime(int(date_str), 1, 1).date()

    #         date_str = date_str.replace('/', '.').replace('-', '.')

    #         for fmt in self.DATE_FORMATS:
    #             try:
    #                 return datetime.strptime(date_str, fmt).date()
    #             except ValueError:
    #                 continue

    #     try:
    #         return datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(date_val) - 2).date()
    #     except (ValueError, TypeError):
    #         return None

    def _clean_phone(self, phone: Optional[str]) -> Optional[str]:
        if not phone or pd.isna(phone):
            return None

        cleaned = self.PHONE_CLEAN_PATTERN.sub("", str(phone))

        if len(cleaned) == 11:
            return cleaned[1:]
        return cleaned
