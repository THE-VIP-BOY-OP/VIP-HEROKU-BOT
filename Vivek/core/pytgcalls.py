import os
import random
from typing import Union

import requests
from ntgcalls import TelegramServerError
from pyrogram import filters
from pyrogram.enums import ParseMode
from pytgcalls import PyTgCalls
from pytgcalls import filters
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

from Vivek.utils.functions import MelodyError, Vivek, chatlist
from Vivek.utils.queue import Queue

from .clients import app

test_stream = "http://docs.evostream.com/sample_content/assets/" "sintel1m720p.mp4"


class MusicPlayer(PyTgCalls):
    def __init__(self):
        super().__init__(app)

    async def play(
        self,
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
            await super().play(chat_id, stream=stream)
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

    async def leave_call(self, chat_id: int):
        try:
            await super().leave_call(chat_id)
        except:
            pass

    async def mute_stream(self, chat_id: int):
        await super().mute_stream(chat_id)

    async def pause_stream(self, chat_id: int):
        await super().pause_stream(chat_id)

    async def resume_stream(self, chat_id: int):
        await super().resume_stream(chat_id)

    async def unmute_stream(self, chat_id: int):
        await super().unmute_stream(chat_id)

    async def seek_stream(self, chat_id, file_path, to_seek, duration, mode):
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
        await super().play(chat_id, stream=stream)

    async def change_stream(self, chat_id):
        mystic = await app.send_message(chat_id, "Downloading Next track from Queue")
        try:

            vidid = (await Queue.get(chat_id)).get("vidid")
            video = (await Queue.get(chat_id)).get("video")
            details = await Queue.next(chat_id)
            file_path = None
            if not details:
                if chat_id not in chatlist:
                    await self.leave_call(chat_id)
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

            if file_path is None or not os.path.isfile(file_path):
                file_path = await Vivek.download(vidid=vidid, video=video)

            await call.play(chat_id, file_path, video)

            await app.send_message(
                chat_id,
                f"<b>Started Streaming</b>\n\n<b>Title</b>: {title}\n<b>Duration</b>: {duration}\n<b>By</b>: {by}",
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML,
            )
            await mystic.delete()
            if by == "ENDLESS PLAY MODE":
                await Queue.add(
                    chat_id,
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
            await self.leave_call(chat_id)

    async def dec(self):

        @super().on_update(filters.stream_end)
        async def my_handler(client: PyTgCalls, update: Update):
            if isinstance(update, (StreamVideoEnded, StreamAudioEnded)):
                await self.change_stream(update.chat_id)

        @super().on_update(fl.chat_update(ChatUpdate.Status.INCOMING_CALL))
        async def incoming_handler(_: PyTgCalls, update: Update):
            await call_py.mtproto_client.send_message(
                update.chat_id,
                "You are calling me!",
            )
            await call.play(
                update.chat_id,
                test_stream,
            )


call = MusicPlayer()
