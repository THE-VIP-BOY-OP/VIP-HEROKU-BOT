from pyrogram import Client
from pytgcalls import PyTgCalls

from config import API_ID, API_HASH, STRING_SESSION

class pytgcall(PyTgCalls):
    def __init__(self):
        self.app = Client(
            "pytgcall",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=STRING_SESSION,
        )
        
        super().__init__(self.app)
