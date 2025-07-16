import hashlib
import hmac
import json
from urllib.parse import unquote


def validate_init_data(init_data: str, bot_token: str):
    vals = {k: unquote(v) for k, v in [s.split("=", 1) for s in init_data.split("&")]}
    if "hash" not in vals:
        return None
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(vals.items()) if k != "hash")
    secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
    h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)
    if h.hexdigest() != vals["hash"]:
        return None
    if "user" in vals:
        user = json.loads(vals["user"])
        return user["id"]
    return None
