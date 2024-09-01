import asyncio

from pyrogram import idle
from Vivek import app, bot, call, HELPABLE
from Vivek.plugins import ALL_MODULES

async def main():

    await app.start()
    await bot.start()
    for all_module in ALL_MODULES:
        imported_module = importlib.import_module("Vivek.plugins" + all_module)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    await call.start()

    await idle()

    await app.stop()
    await bot.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())