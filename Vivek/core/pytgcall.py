from pyrogram import Client
from pytgcalls import PyTgCalls

from config import API_ID, API_HASH, STRING_SESSION

from .clients import app

call = PyTgCalls(app)
