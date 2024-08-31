import asyncio
import logging
import platform

from pyrogram import idle

from bot import app

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler(),
    ],
)


logging.getLogger("pyrogram").setLevel(logging.ERROR)


log = logging.getLogger("U")

async def main():
    log.info("Starting Userbot...")
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
