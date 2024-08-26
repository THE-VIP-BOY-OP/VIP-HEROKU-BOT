import asyncio

import uvloop

uvloop.install()
import logging

from pyrogram import Client, idle

from config import API_HASH, API_ID, BOT_TOKEN, LOG_GROUP_ID

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
    log.info("Starting bot...")
    app = Client(
        "Boss",
        api_id=API_ID,
        api_hash=API_HASH,
        app_version="Boss 2.1.25",
        bot_token=BOT_TOKEN,
        in_memory=True,
        plugins=dict(root="plugins"),
        max_concurrent_transmissions=9,
        lang_pack="android",
        device_model="Boss",
    )
    await app.start()
    log.info("bot started")
    try:
        await app.send_message(LOG_GROUP_ID, "Started")
    except:
        pass
    await idle()
    await app.stop()
    log.info("Stopping bot Good Bye")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
