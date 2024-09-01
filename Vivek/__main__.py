import asyncio
import platform
from pyrogram import idle
from Vivek import app, LOGGER

log = LOGGER("Vivek")

async def main():

    await app.start()
    log.info("Userbot started")
    await idle()
    await app.stop()
    log.info("Stopping bot Good Bye")


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())