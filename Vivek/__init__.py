import uvloop

uvloop.install()

import logging
import os
import shutil
import sys
from os import listdir, mkdir

from Vivek.core.clients import app, bot
from Vivek.utils.filters import edit_filters

from .logger import LOGGER

HELPABLE = {}
edit_filters()


import os
import sys

from pyrogram import Client
from pyrogram import __version__ as v

from config import API_HASH, API_ID, BOT_TOKEN, STRING_SESSION

app = Client(
    name="Vivek",
    api_id=API_ID,
    api_hash=API_HASH,
    app_version=f"Cute {v}",
    session_string=STRING_SESSION,
    in_memory=True,
    plugins=dict(root="Vivek/plugins"),
)
bot = Client(
    name="Vivek1",
    api_id=API_ID,
    api_hash=API_HASH,
    app_version=f"Cute {v}",
    bot_token=BOT_TOKEN,
    in_memory=True,
    plugins=dict(root="Vivek/plugins"),
    max_concurrent_transmissions=9,
)


async def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Vivek", *sys.argv[1:]])


app.bot = bot
app.restart = restart

for file in os.listdir():
    if (
        file.endswith(".jpg")
        or file.endswith(".jpeg")
        or file.endswith(".mp3")
        or file.endswith(".m4a")
        or file.endswith(".mp4")
        or file.endswith(".webm")
        or file.endswith(".png")
        or file.endswith(".session")
        or file.endswith(".session-journal")
    ):
        os.remove(file)

if "downloads" in listdir():
    shutil.rmtree("downloads")
    mkdir("downloads")
