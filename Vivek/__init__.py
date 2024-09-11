import uvloop

uvloop.install()
import logging
import os
import random
import shutil
import sys
from os import listdir, mkdir
from typing import Callable, List, Optional, Union

import pyrogram
import pyromod.listen  # noqa
import requests
from ntgcalls import TelegramServerError
from pyrogram import Client
from pyrogram import __version__ as v
from pyrogram import filters, types
from pyrogram.enums import ParseMode
from pyrogram.filters import Filter
from pytgcalls import PyTgCalls
from pytgcalls import filters as fl
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall
from pytgcalls.types import (
    AudioQuality,
    ChatUpdate,
    MediaStream,
    StreamAudioEnded,
    StreamVideoEnded,
    Update,
    VideoQuality,
)

from config import API_HASH, API_ID, BOT_TOKEN, STRING_SESSION
from Vivek.utils.filters import edit_filters
from Vivek.utils.functions import MelodyError, Vivek, chatlist
from Vivek.utils.queue import Queue

from .logger import LOGGER

HELPABLE = {}
edit_filters()

test_stream = "http://docs.evostream.com/sample_content/assets/" "sintel1m720p.mp4"


app = Client(
    name="Vivek",
    api_id=API_ID,
    api_hash=API_HASH,
    app_version=f"Cute {v}",
    session_string=STRING_SESSION,
    in_memory=True,
    plugins=dict(root="Vivek/plugins"),
)
bot = Client(
    name="Vivek1",
    api_id=API_ID,
    api_hash=API_HASH,
    app_version=f"Cute {v}",
    bot_token=BOT_TOKEN,
    in_memory=True,
    plugins=dict(root="Vivek/plugins"),
    max_concurrent_transmissions=9,
)

call = PyTgCalls(app)


async def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Vivek", *sys.argv[1:]])


app.bot = bot
app.restart = restart
app.call = call


for file in os.listdir():
    if (
        file.endswith(".jpg")
        or file.endswith(".jpeg")
        or file.endswith(".mp3")
        or file.endswith(".m4a")
        or file.endswith(".mp4")
        or file.endswith(".webm")
        or file.endswith(".png")
        or file.endswith(".session")
        or file.endswith(".session-journal")
    ):
        os.remove(file)

if "downloads" in listdir():
    shutil.rmtree("downloads")
    mkdir("downloads")


def ikb(*button_rows):
    """
    Create an inline keyboard with buttons using an even more simplified syntax.
    Automatically defaults to "url" if type is not provided,
    and supports passing rows directly as arguments.

    button_rows: Each row is a list of button parameters like:
    [text, value] or [text, value, type]. If type is omitted, defaults to "url".

    Example:
    ikb(
        ["Google", "https://google.com"],  # Defaults to url
        ["Click Me", "my_callback", "callback"]
    )
    """
    keyboard = []
    for row in button_rows:
        button_row = []
        for button in row:
            text = button[0]
            value = button[1]
            button_type = button[2] if len(button) == 3 else "url"

            if button_type == "url":
                button_row.append(types.InlineKeyboardButton(text=text, url=value))
            elif button_type == "callback":
                button_row.append(
                    types.InlineKeyboardButton(text=text, callback_data=value)
                )
            else:
                raise ValueError("Button type must be either 'url' or 'callback'")

        keyboard.append(button_row)

    return types.InlineKeyboardMarkup(keyboard)


types.ikb = ikb


class MusicPlayer:

    @staticmethod
    async def play(
        chat_id: int,
        file_path: str,
        video: Union[bool, str] = None,
    ):
        if video:
            stream = MediaStream(
                file_path,
                audio_parameters=AudioQuality.STUDIO,
                video_parameters=VideoQuality.FHD_1080p,
            )
        else:
            stream = MediaStream(
                file_path,
                audio_parameters=AudioQuality.STUDIO,
                video_flags=MediaStream.Flags.IGNORE,
            )
        try:
            await call.play(chat_id, stream=stream)
        except NoActiveGroupCall:
            raise MelodyError("There is no active group call.")
        except AlreadyJoinedError as e:
            raise MelodyError(str(e))
        except TelegramServerError:
            raise MelodyError(
                "Telegram is experiencing issues. Please restart the voice chat."
            )
        except Exception as e:
            if "phone.CreateGroupCall" in str(e):
                raise MelodyError("There is no active group call.")
            else:
                raise MelodyError(str(e))

    @staticmethod
    async def leave_call(chat_id: int):
        try:
            await call.leave_call(chat_id)
        except:
            pass

    @staticmethod
    async def mute_stream(chat_id: int):
        await call.mute_stream(chat_id)

    @staticmethod
    async def pause_stream(chat_id: int):
        await call.pause_stream(chat_id)

    @staticmethod
    async def resume_stream(chat_id: int):
        await call.resume_stream(chat_id)

    @staticmethod
    async def unmute_stream(chat_id: int):
        await call.unmute_stream(chat_id)

    @staticmethod
    async def seek_stream(chat_id, file_path, to_seek, duration, mode):
        stream = (
            MediaStream(
                file_path,
                audio_parameters=AudioQuality.STUDIO,
                video_parameters=VideoQuality.FHD_1080p,
                ffmpeg_parameters=f"-ss {to_seek} -to {duration}",
            )
            if mode
            else MediaStream(
                file_path,
                audio_parameters=AudioQuality.HIGH,
                ffmpeg_parameters=f"-ss {to_seek} -to {duration}",
                video_flags=MediaStream.Flags.IGNORE,
            )
        )
        await call.play(chat_id, stream=stream)

    @staticmethod
    async def change_stream(chat_id):
        try:

            vidid = (await Queue.get(chat_id)).get("vidid")
            video = (await Queue.get(chat_id)).get("video")
            chatid = (await Queue.get(chat_id)).get("chatid")
            details = await Queue.next(chat_id)
            file_path = None
            mystic = await app.send_message(chatid, "Downloading Next track from Queue")
            if not details:
                if chat_id not in chatlist:
                    await MusicPlayer.leave_call(chat_id)
                    await Vivek.remove_active_chat(chat_id)
                    return await mystic.edit(
                        "No More songs in Queue. Leaving Voice Chat"
                    )
                else:
                    url = f"https://invidious.jing.rocks/api/v1/videos/{vidid}"
                    response = requests.get(url)
                    video_data = response.json()
                    formats = video_data.get("recommendedVideos", [])
                    list = []
                    for fmt in formats:
                        if (
                            fmt.get("lengthSeconds") is not None
                            and 0 < fmt.get("lengthSeconds") < 420
                        ):
                            a = fmt.get("videoId")
                            list.append(a)
                    vidid = random.choice(list)
                    list.clear()
                    query = f"https://www.youtube.com/watch?v={vidid}"
                    details = await Vivek.track(query)
                    title = details.get("title")
                    duration = details.get("duration_min")
                    vidid = details.get("vidid")
                    by = "ENDLESS PLAY MODE"
            else:
                title = details.get("title")
                duration = details.get("duration")
                vidid = details.get("vidid")
                video = details.get("video")
                file_path = details.get("file_path")
                by = details.get("by")

            if vidid is not None:
                if file_path is None or not os.path.isfile(file_path):
                    file_path = await Vivek.download(vidid=vidid, video=video)

            await MusicPlayer.play(chat_id, file_path, video)

            await app.send_message(
                chatid,
                f"<b>Started Streaming</b>\n\n<b>Title</b>: {title}\n<b>Duration</b>: {duration}\n<b>By</b>: {by}",
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML,
            )
            await mystic.delete()
            if by == "ENDLESS PLAY MODE":
                await Queue.add(
                    chat_id,
                    chatid=chatid,
                    title=title,
                    duration=duration,
                    vidid=vidid,
                    video=video,
                    file_path=file_path,
                    by=by,
                )
        except Exception as e:
            await mystic.edit(e)
            await Vivek.remove_active_chat(chat_id)
            await call.leave_call(chat_id)


@call.on_update(fl.stream_end)
async def my_handler(client: PyTgCalls, update: Update):
    if isinstance(update, (StreamVideoEnded, StreamAudioEnded)):
        await MusicPlayer.change_stream(update.chat_id)
