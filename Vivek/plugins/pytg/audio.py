from pyrogram import filters

from config import LOG_GROUP_ID
from Vivek import app


@app.on_message(filters.sudo & filters.chat(LOG_GROUP_ID) & filters.audio)
async def audio_play(client, message):
    await message.reply_text(message)
