import hmac
import time
from hashlib import sha256
from urllib.parse import urlencode

from core.config import BOT_TOKEN


def create_init_data(user_id: int, username: str = None) -> str:
    auth_date = int(time.time())

    init_data = {"user": f"{user_id}", "auth_date": str(auth_date)}

    if username:
        init_data["username"] = username

    check_string = "\n".join(f"{k}={v}" for k, v in sorted(init_data.items()))

    secret_key = sha256(BOT_TOKEN.encode()).digest()
    hash_ = hmac.new(secret_key, check_string.encode(), sha256).hexdigest()

    init_data["hash"] = hash_

    return urlencode(init_data)
