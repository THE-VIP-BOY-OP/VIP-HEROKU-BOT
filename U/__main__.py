import asyncio

import uvloop
uvloop.install()

from pyrogram import idle
from bot import app

async def main():
    await app.start()
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
