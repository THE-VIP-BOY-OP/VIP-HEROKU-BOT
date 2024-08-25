import uvloop
uvloop.install()

from pyrogram import Client

from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "Boss",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    plugins=dict(root="U/plugins"),
    max_concurrent_transmissions=9,     
)