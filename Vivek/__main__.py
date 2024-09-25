import asyncio
import importlib

from pyrogram import idle

from Vivek import FUNCTIONS, LOGGER, app, modules
from Vivek.plugins import ALL_MODULES

async def main():
    await app.start()  # Starting Userbot client
    LOGGER(__name__).info(f"Userbot started")
    await app.bot.start()  # Starting bot client
    LOGGER(__name__).info(f"Bot started")

    for all_module in ALL_MODULES:
        imported_module = importlib.import_module("Vivek.plugins." + all_module)

        if hasattr(imported_module, "__mod__") and imported_module.__mod__:
            if hasattr(imported_module, "__help__") and imported_module.__help__:
                modules[imported_module.__mod__.lower()] = (
                    imported_module  # Storing the imported module in 'modules' dictionary
                )

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
            FUNCTIONS.append(getattr(imported_module, func))

    await idle()  # Run this bot without stopping
    # Stop the app and bot if keyboard interrupt (CTRL + C PRESSED)
    await app.stop()
    await app.bot.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
