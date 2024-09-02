from pytgcalls import PyTgCalls, filters
from pytgcalls.types import Update

from config import LOG_GROUP_ID
from Vivek.core.pytgcalls import call


@call.on_update(filters.stream_end)
async def my_handler(client: PyTgCalls, update: Update):
    await app.send_message(LOG_GROUP_ID, update)
