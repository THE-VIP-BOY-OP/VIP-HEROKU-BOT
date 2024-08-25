import asyncio
import uvloop

uvloop.install()

import importlib
from pyrogram import idle
from bot import app
from .logging import LOGGER
from config import LOG_GROUP_ID

from U.plugins import ALL_MODULES

log = LOGGER("U")


async def main():
    await app.start()
    log.info(f"Bot Started as {app.me.first_name}")

    """for all_module in ALL_MODULES:
        imported_module = importlib.import_module(all_module)

        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                if imported_module.__MODULE__.lower() not in HELPABLE:
                    HELPABLE[imported_module.__MODULE__.lower()] = imported_module
                else:
                    raise Exception(
                        f"Can't have two modules with name! '{imported_module.__MODULE__}' Please Change One"
                    )"""

    try:
        await app.send_message(LOG_GROUP_ID, "Started")
    except:
        pass
    await idle()
    await app.stop()
    log.info("Stopping bot Good Bye")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
