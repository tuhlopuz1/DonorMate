import csv
import os
import uuid
from typing import Dict, List

import aiofiles


class CSVConverter:
    def __init__(self):
        self.temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
        os.makedirs(self.temp_dir, exist_ok=True)

    async def convert(self, data: List[Dict]) -> str:
        if not data:
            return await self._create_empty_file()

        headers = list(data[0].keys())
        filename = os.path.join(self.temp_dir, f"{uuid.uuid4().hex}.csv")

        async with aiofiles.open(filename, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            await writer.writeheader()
            for row in data:
                await writer.writerow(row)

        return filename

    async def _create_empty_file(self) -> str:
        filename = os.path.join(self.temp_dir, f"{uuid.uuid4().hex}.csv")
        async with aiofiles.open(filename, mode="w"):
            pass
        return filename
