import hashlib
import hmac
from urllib.parse import parse_qsl


def validate_init_data(init_data: str, bot_token: str) -> bool:
    parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    hash_received = parsed_data.pop("hash", None)

    if not hash_received:
        return False

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed_data.items()))

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    hmac_hex = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac.compare_digest(hmac_hex, hash_received)
