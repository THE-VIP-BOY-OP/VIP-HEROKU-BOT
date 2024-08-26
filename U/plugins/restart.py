from pyrogram import filters, Client
import os
import sys


@Client.on_message(filters.command(["restart"]) & filters.me & ~filters.forwarded)
async def _restart(_: Client, message: Message):
    await message.edit("<code>Restarting...</code>")
    os.execvp(sys.executable, [sys.executable, *sys.argv])
