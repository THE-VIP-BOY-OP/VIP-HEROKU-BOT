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
    if platform.python_version_tuple() >= ("3", "11"):
        with asyncio.Runner() as runner:
            loop = runner.get_loop()
            loop.run_until_complete(main())
    else:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(main())
