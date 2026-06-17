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

# If DATABASE_URL is provided (e.g., by Render), use it!
env_db_url = os.getenv("DATABASE_URL")

if env_db_url:
    # SQLAlchemy 1.4+ requires 'postgresql://' instead of 'postgres://'
    if env_db_url.startswith("postgres://"):
        env_db_url = env_db_url.replace("postgres://", "postgresql://", 1)
    DATABASE_URL = env_db_url
else:
    # Fallback to local MySQL setup
    encoded_password = quote_plus(DB_PASSWORD) if DB_PASSWORD else ""
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}"
