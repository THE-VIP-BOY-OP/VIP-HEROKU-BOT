import asyncio
import importlib

from pyrogram import idle

from config import LOG_GROUP_ID
from Vivek import LOGGER, app
from Vivek.plugins import ALL_MODULES


async def main():
    await app.start()



if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
