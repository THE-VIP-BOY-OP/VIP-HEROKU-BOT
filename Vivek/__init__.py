import uvloop
uvloop.install()


from .logging import LOGGER
from Vivek.utils.filters import edit_filters

from pyrogram import __version__ as v
from pyrogram import Client

from config import API_HASH, API_ID, STRING_SESSION, BOT_TOKEN, LOG_GROUP_ID
from pytgcalls import PyTgCalls

from Vivek.utils import VClient
HELPABLE = {}

app = VClient(
    name="Vivek", 
    api_id=API_ID,
    api_hash=API_HASH,
    app_version=f"Cute {v}",
    session_string=STRING_SESSION,
    in_memory=True,
    plugins=dict(root="Vivek/plugins"),
)

bot = VClient(
    name="Vivek1",
    api_id=API_ID,
    api_hash=API_HASH,
    app_version=f"Cute {v}",
    bot_token=BOT_TOKEN,
    in_memory=True,
    plugins=dict(root="Vivek/plugins/bot"),
    max_concurrent_transmissions=9
)

call = PyTgCalls(
    Client(
        name="Vivek", 
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING_SESSION,
    )
)

edit_filters()