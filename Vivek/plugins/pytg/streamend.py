from Vivek.core.pytgcalls import call

from pytgcalls import PyTgCalls, filters
from pytgcalls.types import Update
from pytgcalls.types import MediaStream
from config import LOG_GROUP_ID



@call.on_update(filters.stream_end)
async def my_handler(client: PyTgCalls, update: Update):
    if isinstance(update, StreamVideoEnded):
        await app.send_message(LOG_GROUP_ID, update)