import os
import sys 
from pyrogram import Client
from pyrogram import __version__ as v

from config import API_HASH, API_ID, BOT_TOKEN, STRING_SESSION
from Vivek.utils import VClient

app = Client(
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
    max_concurrent_transmissions=9,
)

async def restart():
    os.execvp(sys.executable, [sys.executable, *sys.argv])

app.bot = bot
app.restart = restart

