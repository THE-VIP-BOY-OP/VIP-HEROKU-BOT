from pyrogram import Client, filters
from pyrogram.types import Message

from Vivek import app
from Vivek.utils import restart

@app.on_message(filters.command(["restart"]) & filters.sudo & ~filters.forwarded)
async def restart(_: Client, message: Message):
    await message.reply_text("<code>Restarting...</code>")
    await restart()
