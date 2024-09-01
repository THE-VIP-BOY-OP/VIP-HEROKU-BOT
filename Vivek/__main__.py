import asyncio
import platform
from pyrogram import idle
from Vivek import app, LOGGER

log = LOGGER(__name__)

async def main():
    await app.start()
    log.info("Userbot started")
    await idle()
    await app.stop()
    log.info("Stopping bot Good Bye")


if __name__ == "__main__":
    app.run(main())
