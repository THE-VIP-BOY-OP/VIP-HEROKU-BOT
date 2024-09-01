from pyrogram import Client
from pytgcalls import PyTgCalls
from Vivek.utils import VClient
from config import API_ID, API_HASH, STRING_SESSION


app = VClient(
            name="Vivek1",
            api_id=API_ID,
            api_hash=API_HASH, 
            session_string=STRING_SESSION,
        )



call = PyTgCalls(app)
