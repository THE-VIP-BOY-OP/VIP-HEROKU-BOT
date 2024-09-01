from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID", ))
API_HASH = getenv("API_HASH", "")
STRING_SESSION = getenv("STRING_SESSION", None)
BOT_TOKEN = getenv("BOT_TOKEN", "")
LOG_GROUP_ID = getenv("LOG_GROUP_ID", -1002146211959)
OWNER_ID = list(
    map(int, getenv("OWNER_ID", "6815918609 7301077117 7428672286").split())
)


PREFIX = list(map(str, getenv("PREFIX", ". ! /").split()))
