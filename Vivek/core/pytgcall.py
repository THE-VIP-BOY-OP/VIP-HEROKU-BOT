from pyrogram import Client
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, STRING_SESSION


class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client(
            name="String1",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=str(STRING_SESSION),
        )
        self.one = PyTgCalls(
            self.userbot1,
            cache_duration=100,
        )
 
    async def start(self):
        await self.one.start()


call = Call()