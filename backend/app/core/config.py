import logging
import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Environment loaded")


DB_URL = os.getenv("DB_URL")
RANDOM_SHA = os.getenv("RANDOM_SHA")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DBNAME = os.getenv("POSTGRES_DBNAME")
BOT_TOKEN = os.getenv("BOT_TOKEN")
RABBITMQ_URL = os.getenv("RABBITMQ_URL")

if DB_URL:
    DATABASE_URL = DB_URL
else:
    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"  # noqa

logger.info(DATABASE_URL)
