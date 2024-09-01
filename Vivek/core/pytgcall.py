from pyrogram import Client
from pytgcalls import PyTgCalls

from config import API_ID, API_HASH, STRING_SESSION

from .clients import app


"""class pytgcall(PyTgCalls):
    def __init__(self):
        super().__init__(
            Client(
                name="pytgcall",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=STRING_SESSION
            )
        )

call = pytgcall()"""

call = PyTgCalls(app)
