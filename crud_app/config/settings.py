import os
from dotenv import load_dotenv


load_dotenv()


NEW_RELIC_LICENSE_KEY = os.getenv(
    "NEW_RELIC_LICENSE_KEY"
)

NEW_RELIC_USER_KEY = os.getenv(
    "NEW_RELIC_USER_KEY"
)

NEW_RELIC_ACCOUNT_ID = os.getenv(
    "NEW_RELIC_ACCOUNT_ID"
)

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "newrelic_tickets")

from urllib.parse import quote_plus
encoded_password = quote_plus(DB_PASSWORD) if DB_PASSWORD else ""
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}"
