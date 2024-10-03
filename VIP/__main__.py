import asyncio
import importlib

from pyrogram import idle

from VIP import app
from VIP.plugins import ALL_MODULES


async def main():
    await app.start()
    for all_module in ALL_MODULES:
        imported_module = importlib.import_module("VIP.plugins" + all_module)

    await idle()
    await app.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
