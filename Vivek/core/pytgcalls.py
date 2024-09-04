import os
from typing import Union

from ntgcalls import TelegramServerError
from pyrogram.enums import ParseMode
from pytgcalls import PyTgCalls, filters
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall
from pytgcalls.types import AudioQuality, MediaStream, Update, VideoQuality
from pytgcalls.types.stream import StreamAudioEnded, StreamVideoEnded

from Vivek.utils.functions import MelodyError, Vivek
from Vivek.utils.queue import Queue

from .clients import app


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
        details = await Queue.next(chat_id)
        if not details or details is None:
            await self.leave_call(chat_id)
            await Vivek.remove_active_chat(chat_id)
            return await mystic.edit("No More songs in Queue. Leaving Voice Chat")

        title = details.get("title")
        duration = details.get("duration")
        vidid = details.get("vidid")
        video = details.get("video")
        file_path = details.get("file_path")
        by = details.get("by")

        if not os.path.isfile(file_path):
            file_path = await Vivek.download(vidid=vidid, video=video)

        try:
            await call.play(chat_id, file_path, video)
        except MelodyError as e:
            return await mystic.edit(f"Error: {e}")
        except Exception as e:
            return await mystic.edit(f"Unexpected Error: {e}")

        await app.send_message(
            chat_id,
            f"<b>Started Streaming</b>\n\n<b>Title</b>: {title}\n<b>Duration</b>: {duration}\n<b>By</b>: {by}",
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML,
        )
        await mystic.delete()

    async def dec(self):

        @super().on_update(filters.stream_end)
        async def my_handler(client: PyTgCalls, update: Update):
            if isinstance(update, (StreamVideoEnded, StreamAudioEnded)):
                await self.change_stream(update.chat_id)


call = MusicPlayer()
