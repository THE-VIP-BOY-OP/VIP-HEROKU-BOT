import uvloop
uvloop.install()

import importlib

from pyrogram import __version__ as v
from Vivek.utils import VClient
from Vivek.logging import LOGGER

from config import API_HASH, API_ID, STRING_SESSION, BOT_TOKEN, LOG_GROUP_ID

from Vivek.plugins import ALL_MODULES

HELPABLE = {}

class Vivek(VClient):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot")
        super().__init__(
            name="Vivek", 
            api_id=API_ID,
            api_hash=API_HASH,
            app_version=f"Cute {v}",
            session_string=STRING_SESSION,
            #in_memory=True,
            plugins=dict(root="Vivek/plugins"),
            max_concurrent_transmissions=9,
        )

        self.bot = VClient(
            name="Vivek1",
            api_id=API_ID,
            api_hash=API_HASH,
            app_version=f"Cute {v}",
            bot_token=BOT_TOKEN,
            in_memory=True,
            plugins=dict(root="Vivek/plugins/bot"),
            max_concurrent_transmissions=9
        )

    async def import_all_module(self):
        for all_module in ALL_MODULES:
            imported_module = importlib.import_module("Vivek.plugins" + all_module)

            if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
                if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                    HELPABLE[imported_module.__MODULE__.lower()] = imported_module


    async def start(self):
        await super().start()
        LOGGER(__name__).info(f"UserBot Started")
        #await self.bot.start()
        #LOGGER(__name__).info(f"Helper Bot Started")
        #await self.bot.send_message(LOG_GROUP_ID, "Bot has Started Successfully")
    async def stop(self):
        LOGGER(__name__).info(f"Stopping! Radhe Radhe")
        await super().stop()
        #await self.bot.stop()
           