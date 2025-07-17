import csv
import os
import uuid
import aiofiles
from typing import List, Dict


class CSVConverter:
    def __init__(self):
        self.temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
        os.makedirs(self.temp_dir, exist_ok=True)

    async def convert(self, data: List[Dict]) -> str:
        """Конвертирует список словарей в CSV файл и возвращает путь к файлу"""
        if not data:
            return await self._create_empty_file()

        headers = list(data[0].keys())
        filename = os.path.join(self.temp_dir, f"{uuid.uuid4().hex}.csv")

        async with aiofiles.open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            await writer.writeheader()
            for row in data:
                await writer.writerow(row)

        return filename

    async def _create_empty_file(self) -> str:
        """Создает пустой CSV файл для пустых данных"""
        filename = os.path.join(self.temp_dir, f"{uuid.uuid4().hex}.csv")
        async with aiofiles.open(filename, mode='w') as f:
            pass  # Создаем пустой файл
        return filename
    
