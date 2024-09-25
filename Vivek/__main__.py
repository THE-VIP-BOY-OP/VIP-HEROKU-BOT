import asyncio
import importlib

from pyrogram import idle

from Vivek import FUNCTIONS, LOGGER, app
from Vivek.plugins import ALL_MODULES


async def main():
    await app.start()  # Starting Userbot client
    LOGGER(__name__).info(f"Userbot started")
    FUNCTIONS["MODULES"] = []

    for all_module in ALL_MODULES:
        imported_module = importlib.import_module("Vivek.plugins" + all_module)

        functions = [
            func
            for func in dir(imported_module)
            if callable(getattr(imported_module, func))
        ]
        handlers = [
            func
            for func in functions
            if hasattr(getattr(imported_module, func), "handlers")
        ]
        for func in handlers:
            FUNCTIONS["MODULES"].append(getattr(imported_module, func))
    FUNCTIONS["LOADED"] = FUNCTIONS["MODULES"].copy()
    await idle()  # Run this bot without stopping
    # Stop the app and bot if keyboard interrupt (CTRL + C PRESSED)
    await app.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
