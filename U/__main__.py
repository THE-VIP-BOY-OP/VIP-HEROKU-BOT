import asyncio

import uvloop
uvloop.install()

from pyrogram import idle
from bot import app

from .logging import LOGGER
log = LOGGER("U")

async def main():
    
    log.info("Starting bot....")

    await app.start()
    log.info(f"bot Started as {app.me.first_name}")

    await idle()
    await app.stop()
    log.info("Stopping bot Good Bye")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
