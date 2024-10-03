from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = int(
    getenv(
        "API_ID",
    )
)

API_HASH = getenv("API_HASH", "")

BOT_TOKEN = getenv("BOT_TOKEN", None)

HEROKU_API_KEY = getenv("HEROKU_API_KEY", "")

OWNER_ID = list(
    map(int, getenv("OWNER_ID", "6815918609 7482534247").split())
)
