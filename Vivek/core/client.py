import importlib

import pyromod.listen  # noqa
from pyrogram import __version__ as v

from config import API_HASH, API_ID, BOT_TOKEN, STRING_SESSION
from Vivek.functions.client import VClient

from .logger import LOGGER


class App(VClient):
    def __init__(self):
        LOGGER(__name__).info("Starting user and bot client")
        super().__init__(
            name="Vivek",
            api_id=API_ID,
            api_hash=API_HASH,
            app_version=f"Cute {v}",
            session_string=STRING_SESSION,
            in_memory=True,
        )

        self.bot = VClient(
            name="Vivek1",
            api_id=API_ID,
            api_hash=API_HASH,
            app_version=f"Cute {v}",
            bot_token=BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=9,
        )

    async def start(self):
        await super().start()
        LOGGER(__name__).info(f"Userbot started")
        await self.bot.start()
        LOGGER(__name__).info(f"bot started")
        for all_module in ALL_MODULES:
            importlib.import_module("Vivek.plugins" + all_module)

    async def stop(self):
        await super().stop()
        await self.bot.stop()


app = App()
