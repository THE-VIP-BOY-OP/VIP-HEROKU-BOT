from pyrogram import __version__ as v
from config import API_HASH, API_ID, STRING_SESSION
import platform
import asyncio

from utils import Client
import uvloop

uvloop.install()


class Vivek(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot")
        super().__init__(
            "Vivek", 
            api_id=API_ID,
            api_hash=API_HASH,
            app_version=f"Cute {v}",
            session_string=STRING_SESSION,
            in_memory=True,
            plugins=dict(root="Vivek/plugins"),
            max_concurrent_transmissions=9,
        )


    def run(self, main):
        if platform.python_version_tuple() >= ("3", "11"):
            with asyncio.Runner() as runner:
                loop = runner.get_loop()
                loop.run_until_complete(main())
        else:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(main())
      
