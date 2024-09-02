from pyrogram import filters
from Vivek import app
from config import LOG_GROUP_ID

@app.on_message(filters.sudo & filters.chat(LOG_GROUP_ID) & filters.audio)
async def audio_play(client, message):
    await message.reply_text(message)
