from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

API_ID = int(getenv("API_ID", 25488022))
API_HASH = getenv("API_HASH", "0c999a454fddd79251213be7944811e8")
STRING_SESSION = getenv("STRING_SESSION", None)
LOG_GROUP_ID = getenv("LOG_GROUP_ID", -1002042572827)
OWNER_ID = list(map(int, getenv("OWNER_ID", "6815918609 7301077117 7428672286").split()))
PREFIX = list(map(str, getenv("PREFIX", ". ! /").split()))
