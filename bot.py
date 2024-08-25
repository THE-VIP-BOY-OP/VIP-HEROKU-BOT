import asyncio

import uvloop
uvloop.install()

import logging
from pyrogram import Client, idle

from config import API_ID, API_HASH, BOT_TOKEN

log = logging.getLogger(__name__)

async def main():

    app = Client(
        "Boss",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        in_memory=True,
        plugins=dict(root="plugins"),
        max_concurrent_transmissions=9,     
    )

    log.info("Starting bot")

    await app.start()
    await idle()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())