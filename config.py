from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

API_ID = int(getenv("API_ID", 25488022))

API_HASH = getenv("API_HASH", "0c999a454fddd79251213be7944811e8")

STRING_SESSION = getenv("STRING_SESSION", None)

LOG_GROUP_ID = getenv("LOG_GROUP_ID", 6815918609)

OWNER_ID = getenv("OWNER_ID", 6815918609)

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/VivekKumar-IN/U")

UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")

GIT_TOKEN = getenv("GIT_TOKEN", None)

START_IMAGE = getenv("START_IMAGE", None)

BANNED_USERS = filters.user()
PREFIX = list(map(int, getenv("PREFIX", ". ! ").split()))
