import asyncio
import importlib
from typing import Awaitable, Callable

import pyromod.listen  # noqa
from pyrogram import __version__ as v
from pyrogram import idle

from config import API_HASH, API_ID, BOT_TOKEN, LOG_GROUP_ID, STRING_SESSION
from Vivek.functions.client import VClient
from Vivek.plugins import ALL_MODULES

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
        await super().load_database()
        await app.bot.send_message(LOG_GROUP_ID, "started")
        LOGGER(__name__).info(f"bot started")
        for all_module in ALL_MODULES:
            importlib.import_module("Vivek.plugins" + all_module)
        await idle()
        await self.stop()

    async def stop(self):
        LOGGER(__name__).info(f"Radhe Radhe\nStopping....")
        await super().stop()
        await self.bot.stop()

    def run(self, fnc: Callable[[], Awaitable[None]]):
        asyncio.get_event_loop_policy().get_event_loop().run_until_complete(fnc())


app = App()
