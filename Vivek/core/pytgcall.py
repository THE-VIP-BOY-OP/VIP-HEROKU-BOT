from pyrogram import Client
from pytgcalls import PyTgCalls

from config import API_ID, API_HASH, STRING_SESSION

from Vivek import app 

class pytgcall(PyTgCalls):
    def __init__(self, app:Client):
        super().__init__(app)

call = pytgcall(app)
