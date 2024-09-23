import asyncio

from pyrogram import idle

from config import LOG_GROUP_ID
from Vivek import LOGGER, app
from Vivek.plugins import ALL_MODULES

from .logger import LOGGER


async def main():
    await app.start()  # Starting Userbot client
    LOGGER(__name__).info(f"Userbot started")
    await app.bot.start()  # Starting bot client
    await app.bot.send_message(LOG_GROUP_ID, "started")
    LOGGER(__name__).info(f"bot started")
    for all_module in ALL_MODULES:
        importlib.import_module("Vivek.plugins" + all_module)
    await idle()  # Run this bot without stopping
    # Stop the app and bot if keyboard interrupt (CTRL + C PRESSED)
    await app.stop()
    await app.bot.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
