from pyrogram import filters

from config import LOG_GROUP_ID
from Vivek import app


@app.on_message(filters.sudo & filters.chat(LOG_GROUP_ID) & (filters.audio | filters.voice))
async def audio_play(client, message):
    if message.audio:
        await message.reply_text(message.audio.file_id)
    if message.voice:
        await message.reply_text(message.voice.file_id)
