from pyrogram import __version__ as v
from config import API_HASH, API_ID, STRING_SESSION
import platform
import asyncio

from utils import Client
import uvloop

uvloop.install()

class Vivek(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot")
        super().__init__(
            "Vivek", 
            api_id=API_ID,
            api_hash=API_HASH,
            app_version=f"Cute {v}",
            session_string=STRING_SESSION,
            in_memory=True,
            plugins=dict(root="Vivek/plugins"),
            max_concurrent_transmissions=9,
        )

    self.bot = Client(
                    "Vivek1",
                    api_id=API_ID,
                    api_hash=API_HASH,
                    app_version=f"Cute {v}",
                    bot_token=BOT_TOKEN,
                    in_memory=True,
                    plugins=dict(root="Vivek/plugins/bot"),
                    max_concurrent_transmissions=9,)
           