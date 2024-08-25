import asyncio

import uvloop
uvloop.install()

from pyrogram import idle
from bot import app

from .logging import LOGGER
log = LOGGER("U")

from config import LOG_GROUP_ID

async def main():
    
    log.info("Starting bot....")

    await app.start()
    log.info(f"bot Started as {app.me.first_name}")
    try:
        await app.send_message(LOG_GROUP_ID, "Started"
    except:
        pass
    await idle()
    await app.stop()
    log.info("Stopping bot Good Bye")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
