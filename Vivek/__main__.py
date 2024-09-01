import asyncio
import importlib
from pyrogram import idle
from Vivek import app


async def main():

    await app.start()
    for module in ALL_MODULES:
        importlib.import_module("Vivek.plugins" + module)
    await idle()
    await app.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())