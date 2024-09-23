import uvloop

uvloop.install()  # Applying uvloop event loop policy
from pyrogram import __version__ as v

from config import API_HASH, API_ID, BOT_TOKEN, LOG_GROUP_ID, STRING_SESSION
from Vivek.functions.client import VClient  # This is pyrogram modified Client

from .functions import (  # functions for editing pyrogram filters or for removing media's on starting
    dir,
    edit_filters,
)
from .functions.logger import LOGGER  # Logger

dir()
edit_filters()
app = Vclient(
    name="Vivek",
    api_id=API_ID,
    api_hash=API_HASH,
    app_version=f"Cute {v}",
    session_string=STRING_SESSION,
    in_memory=True,
)

# Initialising bot client as app.bot
app.bot = VClient(
    name="Vivek1",
    api_id=API_ID,
    api_hash=API_HASH,
    app_version=f"Cute {v}",
    bot_token=BOT_TOKEN,
    in_memory=True,
    max_concurrent_transmissions=9,
)
