import os

import ffmpeg
from pyrogram import filters

from config import LOG_GROUP_ID
from Vivek import app, MusicPlayer
from Vivek.utils.functions import S12K, Vivek
from Vivek.utils.queue import Queue


@app.on_message(filters.chat(LOG_GROUP_ID) & (filters.audio | filters.voice))
async def audio_play(client, message):
    if message.audio:
        file_path = message.audio.file_id
        file_name = message.audio.file_name
    if message.voice:
        file_path = message.voice.file_id
        file_name = f"{message.voice.file_unique_id}.ogg"

    a = await app.download_media(file_path)

    (
        ffmpeg.input(a)
        .filter("volume", "18dB")
        .output(file_name)
        .overwrite_output()
        .run()
    )
    chat_id = S12K()
    await MusicPlayer.play(chat_id, file_name)
    await message.reply_text("Started Playing")
    os.remove(a)
    os.remove(file_name)


@app.on_message(filters.sudo & filters.command("playhere"))
async def audio_play(client, message):
    S12K(message.chat.id)
    await message.reply_text(
        "Now All recieved audio/voice has been playing here from since Now"
    )


@app.on_message(filters.sudo & filters.command("end"))
async def audio_play(client, message):
    chat_id = message.chat.id
    await MusicPlayer.leave_call(chat_id)
    await Queue.clear(chat_id)
    await Vivek.remove_active_chat(chat_id)
