import hmac
import json
import time
from datetime import datetime
from hashlib import sha256
from urllib.parse import urlencode
from uuid import UUID

import aiohttp
from core.config import BACKEND_URL, BOT_TOKEN


def create_init_data(user_id: int, username: str = None) -> str:
    auth_date = int(time.time())

    user_data = {"id": user_id}
    if username:
        user_data["username"] = username

    init_data = {"user": json.dumps(user_data, separators=(",", ":")), "auth_date": str(auth_date)}

    check_string = "\n".join(f"{k}={v}" for k, v in sorted(init_data.items()))
    secret_key = hmac.new("WebAppData".encode(), BOT_TOKEN.encode(), sha256).digest()
    hash_ = hmac.new(secret_key, check_string.encode(), sha256).hexdigest()

    init_data["hash"] = hash_

    return urlencode(init_data)


async def forward_exemption_to_fastapi(
    token: str,
    start_date: datetime,
    end_date: datetime,
    file_id: str,
    file_name: str,
    mime_type: str,
    medic_phone_num: str = None,
    comment: str = None,
):
    from core.dispatcher import bot

    file_info = await bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as tg_response:
            file_bytes = await tg_response.read()

        form = aiohttp.FormData()
        form.add_field("start_date", start_date.isoformat() if isinstance(start_date, datetime) else start_date)
        form.add_field("end_date", end_date.isoformat() if isinstance(end_date, datetime) else end_date)

        if medic_phone_num is not None:
            form.add_field("medic_phone_num", medic_phone_num)
        if comment is not None:
            form.add_field("comment", comment)

        form.add_field(
            "file",
            file_bytes,
            filename=file_name,
            content_type=mime_type or "application/octet-stream",
        )

        headers = {"Authorization": f"Bearer {token}"}

        async with session.post(f"{BACKEND_URL}/upload-medical-exemption", data=form, headers=headers) as resp:
            return await resp.json()


async def get_access_token(chat_id: int, chat_username: str = None):
    init_data = create_init_data(chat_id, chat_username)
    print(">>> initData:", init_data)
    async with aiohttp.ClientSession() as session:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"initData": init_data}
        async with session.post(f"{BACKEND_URL}/get-token", data=data, headers=headers) as response:
            if response.status != 200:
                raise Exception(f"Token request failed: {response.status}")
            tokens = await response.json()
            return str(tokens["access"])


async def check_notifications(chat_id: int, reg_id: UUID):
    token = await get_access_token(chat_id=chat_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{BACKEND_URL}/check-notific/{reg_id}", headers={"Authorization": f"Bearer {token}"}
        ) as resp:
            if resp.status == 200:
                return True
            else:
                return False
