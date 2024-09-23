import uvloop

# Applying uvloop event loop policy

uvloop.install()

from Vivek.functions.client import VClient  # This is pyrogram modified Client

from .functions import dir, edit_filters

# Logger
from .functions.logger import LOGGER

# functions for editing pyrogram filters or for removing media's on starting


dir()
edit_filters()

import pyromod.listen  # noqa
from pyrogram import __version__ as v

from config import API_HASH, API_ID, BOT_TOKEN, LOG_GROUP_ID, STRING_SESSION

app = Vclient(
    name="Vivek",
    api_id=API_ID,
    api_hash=API_HASH,
    app_version=f"Cute {v}",
    session_string=STRING_SESSION,
    in_memory=True,
)

app.bot = VClient(
    name="Vivek1",
    api_id=API_ID,
    api_hash=API_HASH,
    app_version=f"Cute {v}",
    bot_token=BOT_TOKEN,
    in_memory=True,
    max_concurrent_transmissions=9,
)
