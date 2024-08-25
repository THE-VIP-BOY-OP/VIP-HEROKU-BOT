from os import getenv

from dotenv import load_dotenv

API_ID = int(getenv("API_ID", 25488022))

API_HASH = getenv("API_HASH", "0c999a454fddd79251213be7944811e8")

BOT_TOKEN = getenv("BOT_TOKEN", "6751747123:AAH4631aqVNXv01XufsLFQgWLLkgtU_Du-E")

LOG_GROUP_ID = getenv("LOG_GROUP_ID", -1002042572827)

OWNER_ID = getenv("OWNER_ID", 6815918609)

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/VivekKumar-IN/U")

UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")

GIT_TOKEN = getenv("GIT_TOKEN", "")