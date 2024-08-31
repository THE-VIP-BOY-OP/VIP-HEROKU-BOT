from pyrogram import __version__ as v
import uvloop
from config import API_HASH, API_ID, STRING_SESSION
from utils import Client

uvloop.install()

app = Client(
    "Boss", 
    api_id=API_ID,
    api_hash=API_HASH,
    app_version=f"Cute {v}",
    session_string=STRING_SESSION,
    in_memory=True,
    plugins=dict(root="plugins"),
    max_concurrent_transmissions=9,
)