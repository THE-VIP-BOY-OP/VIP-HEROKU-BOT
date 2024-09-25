import uvloop

uvloop.install()  # Applying uvloop event loop policy

import os
import shutil

from pyrogram import __version__ as v

from config import API_HASH, API_ID, BOT_TOKEN, LOG_GROUP_ID, STRING_SESSION
from Vivek.functions.client import VClient  # This is pyrogram modified Client

from .functions import edit_filters
from .functions.logger import LOGGER  # Logger

edit_filters()  # Editing Some Pyrogram Filters
modules = {}  # stored loaded modules that will use for creating help or load/unload

app = VClient(
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

files = [
    ".jpg",
    ".jpeg",
    ".mp3",
    ".m4a",
    ".mp4",
    ".webm",
    ".png",
    ".session",
    ".session-journal",
]

for file in os.listdir():
    if any(file.endswith(ext) for ext in files):
        os.remove(file)

if "downloads" in os.listdir():
    shutil.rmtree("downloads")
    os.mkdir("downloads")
