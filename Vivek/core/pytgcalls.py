from typing import Union

from ntgcalls import TelegramServerError
from pytgcalls import PyTgCalls, filters
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall
from pytgcalls.types import AudioQuality, MediaStream, Update, VideoQuality
from pytgcalls.types.stream import StreamAudioEnded, StreamVideoEnded

from Vivek.utils.functions import MelodyError

from .clients import app

from Vivek.utils.functions import Vivek
from Vivek.utils.queue import Queue
import os

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
                audio_parameters=AudioQuality.HIGH,
                video_parameters=VideoQuality.SD_480p,
            )
        else:
            stream = MediaStream(
                file_path,
                audio_parameters=AudioQuality.HIGH,
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
        await 
super().unmute_stream(chat_id)

    async def change_stream(chat_id):
    	mystic = await app.send_message(chat_id, "Downloading Next track from Queue")
        details = await Queue.next(chat_id)
        if not details:
        	await Vivek.remove_active_chat(chat_id)
            await mystic.edit(chat_id, "No More songs in Queue Leaving Voice Chat")
            return await self.leave_call(chat_id)
        
        title = details.get('title')
        duration = details.get('duration')
        vidid = details.get('vidid')
        video = details.get('video')
        file_path = details.get('file_path')
        by = details.get('by')
        if not os.path.isfile(file_path):
        	file_path = await Vivek.download(vidid=vidid, video=video)
        try:
            await call.play(message.chat.id, file_path, video)
        except MelodyError as e:
                return await mystic.edit(e)
        except Exception as e:
            return await mystic.edit(e)
        await app.send_message(
            message.chat.id,
            f"**Started Streaming**\n\nTitle: {title}\nDuration: {duration}\n by {by}",
            disable_web_page_preview=True,
        )
    

    async def dec(self):
        @super().on_update(filters.stream_end)
        async def my_handler(client: PyTgCalls, update: Update):
            if isinstance(update, (StreamVideoEnded, StreamAudioEnded)):
                await self.leave_call(update.chat_id)


call = MusicPlayer()
