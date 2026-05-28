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
