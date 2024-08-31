import asyncio
import logging
import platform

from pyrogram import idle

from pyrogram import __version__ as v
import uvloop
from config import API_HASH, API_ID, STRING_SESSION
from utils import Client

uvloop.install()



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
    app = Client(
        "Boss", 
        api_id=API_ID,
        api_hash=API_HASH,
        app_version=f"Cute {v}",
        session_string=STRING_SESSION,
        in_memory=True,
        plugins=dict(root="plugins"),
        max_concurrent_transmissions=9,
    )
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
