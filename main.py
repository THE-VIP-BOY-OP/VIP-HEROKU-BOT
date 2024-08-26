import asyncio
import uvloop

uvloop.install()

from pyrogram import Client, idle
from logging import LOGGER
from config import LOG_GROUP_ID

log = LOGGER("U")
from config import API_ID, API_HASH, BOT_TOKEN


async def main():
    log.info("Starting bot...")
    app = Client(
        "Boss",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        in_memory=True,
        plugins=dict(root="U/plugins"),
        max_concurrent_transmissions=9,
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
