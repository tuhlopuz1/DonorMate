import hashlib
import hmac
import logging
from urllib.parse import parse_qsl


def validate_init_data(init_data: str, bot_token: str) -> bool:
    logging.info("Received initData:", init_data)
    parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    logging.info("Parsed data:", parsed_data)
    hash_received = parsed_data.pop("hash", None)
    logging.info("Received hash:", hash_received)

    if not hash_received:
        return False

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed_data.items()))
    logging.info("Data check string:", repr(data_check_string))

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    hmac_hex = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    logging.info("Calculated hash:", hmac_hex)

    return hmac.compare_digest(hmac_hex, hash_received)
