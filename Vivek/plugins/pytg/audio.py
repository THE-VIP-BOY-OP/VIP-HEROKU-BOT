import os
from pyrogram import filters

from config import LOG_GROUP_ID
from Vivek import app
from Vivek.utils.functions import S12K
from Vivek.core.pytgcalls import call

@app.on_message(
    filters.sudo & filters.chat(LOG_GROUP_ID) & (filters.audio | filters.voice)
)
async def audio_play(client, message):
    if message.audio:
        file_path = message.audio.file_id
    if message.voice:
        file_path = message.voice.file_id
    a = await app.download_media(file_path)
    chat_id = S12K()
    await call.play(chat_id, a)
    await message.reply_text("Started Playing")
    os.remove(a)
    

@app.on_message(
    filters.sudo & filters.command("playhere")
)
async def audio_play(client, message):
    S12K(message.chat.id)
    await message.reply_text("Now All recieved audio/voice has been playing here from since Now")