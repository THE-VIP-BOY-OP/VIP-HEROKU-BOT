import uvloop
uvloop.install()

from pyrogram import __version__ as v
from Vivek.utils import Client
from Vivek.logging import LOGGER

from config import API_HASH, API_ID, STRING_SESSION, BOT_TOKEN, LOG_GROUP_ID


class Vivek(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot")
        super().__init__(
            name="Vivek", 
            api_id=API_ID,
            api_hash=API_HASH,
            app_version=f"Cute {v}",
            session_string=STRING_SESSION,
            in_memory=True,
            plugins=dict(root="Vivek/plugins"),
            max_concurrent_transmissions=9,
        )

        self.bot = Client(
                name="Vivek1",
                api_id=API_ID,
                api_hash=API_HASH,
                app_version=f"Cute {v}",
                bot_token=BOT_TOKEN,
                in_memory=True,
                plugins=dict(root="Vivek/plugins/bot"),
                max_concurrent_transmissions=9
            )

    async def start(self):
        await super().start()
        LOGGER(__name__).info(f"UserBot Started")
        await self.bot.start()
        LOGGER(__name__).info(f"Helper Bot")
        await self.bot.send_message(LOG_GROUP_ID, "Bot has Started Successfully")
    async def stop(self):
        LOGGER(__name__).info(f"Stopping! Radhe Radhe")
        await super().stop()
        await self.bot.stop()
           