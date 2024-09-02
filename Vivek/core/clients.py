from pyrogram import Client
from pyrogram import __version__ as v

from pytgcalls import PyTgCalls

from config import API_HASH, API_ID, BOT_TOKEN, STRING_SESSION
from Vivek.utils import VClient

"""app = Client(
    name="Vivek",
    api_id=API_ID,
    api_hash=API_HASH,
    app_version=f"Cute {v}",
    session_string=STRING_SESSION,
    in_memory=True,
    plugins=dict(root="Vivek/plugins"),
)

bot = VClient(
    name="Vivek1",
    api_id=API_ID,
    api_hash=API_HASH,
    app_version=f"Cute {v}",
    bot_token=BOT_TOKEN,
    in_memory=True,
    plugins=dict(root="Vivek/plugins/bot"),
    max_concurrent_transmissions=9,
)"""

class App(Client):
    def __init__(self):
        super().__init__(
            name="Vivek",
            api_id=API_ID,
            api_hash=API_HASH,
            app_version=f"Cute {v}",
            session_string=STRING_SESSION,
            in_memory=True,
            plugins=dict(root="Vivek/plugins"),
        )
        self.call = PyTgCalls(self)
        self.bot = VClient(
            name="Vivek1",
            api_id=API_ID,
            api_hash=API_HASH,
            app_version=f"Cute {v}",
            bot_token=BOT_TOKEN,
            in_memory=True,
            plugins=dict(root="Vivek/plugins/bot"),
            max_concurrent_transmissions=9,
        )

    async def start(self):
        await super().start()
        await self.call.start()

app = App()
        
