import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import JWTError, jwt

from app.core.config import RANDOM_SHA


class TokenManager:
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 90
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 60

    @staticmethod
    def create_token(data: Dict[str, Any], access: bool = True) -> str:
        to_encode = data.copy()
        if access:
            to_encode["type"] = "access"
            expire = datetime.now(timezone.utc) + timedelta(minutes=TokenManager.ACCESS_TOKEN_EXPIRE_MINUTES)
        else:
            to_encode["type"] = "refresh"
            expire = datetime.now(timezone.utc) + timedelta(minutes=TokenManager.REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            RANDOM_SHA,
            algorithm=TokenManager.ALGORITHM,
        )
        return encoded_jwt

    @staticmethod
    def decode_token(token: str, access: bool = True) -> Dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                RANDOM_SHA,
                algorithms=[TokenManager.ALGORITHM],
            )

            if datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc) < datetime.now(timezone.utc):
                logging.info("Token has expired")
                return False
            if access and "type" != "access":
                logging.info("Invalid token type")
                return False
            elif not access and "type" != "refresh":
                logging.info("Invalid token type")
                return False
            return payload
        except JWTError as e:
            logging.info(f"error: {e}")
            return False
