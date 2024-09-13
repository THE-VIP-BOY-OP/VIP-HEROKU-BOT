        "API_ID",
    )
    getenv(
    map(int, getenv("OWNER_ID", "6815918609 7301077117 7428672286").split())
)
)
API_HASH = getenv("API_HASH", "")
API_ID = int(
BOT_TOKEN = getenv("BOT_TOKEN", "")
GIT_TOKEN = getenv("GIT_TOKEN", "")
LOG_GROUP_ID = getenv("LOG_GROUP_ID", -1002146211959)
ONLY_FOR_SUDO = bool(getenv("ONLY_FOR_SUDO", True))
OWNER_ID = list(
PREFIX = list(map(str, getenv("PREFIX", "!").split()))
STRING_SESSION = getenv("STRING_SESSION", None)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/Vivekkumar-IN/Vivek")
from dotenv import load_dotenv
from os import getenv
load_dotenv()













