from typing import Union
from pytgcalls import PyTgCalls
from pytgcalls.types import (
    MediaStream,
    AudioQuality, 
    VideoQuality,
    Update,
)

from Vivek.utils.functions import (
    is_music_playing,
    music_off,
    music_on,
    MelodyError,
)

from .clients import app


class MusicPlayer(PyTgCalls):
    def __init__(self):
        super().__init__(app)

    async def play(
        self, 
        file_path: str, 
        chat_id: int, 
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
            )
        try:
            await self.play(chat_id, stream)
            await add_active_chat(chat_id)
        except NoActiveGroupCall:
            raise MelodyError("There Are No active Group Call")
        except AlreadyJoinedError as e:
            raise MelodyError(e)
        except TelegramServerError:
            raise MelodyError("Telegram Has Suffering from Some Problems Please Restart The Voice Chat")
        except Exception as e:
            if "phone.CreateGroupCall" in str(e):
            	raise MelodyError("There Are No active Group Call")
            else:
            	raise MelodyError(e)

    async def leave_call(self, chat_id: int):
    	try:
    	    await remove_active_chat(chat_id)
            await self.leave_call(chat_id)
        except:
        	pass

    async def mute_stream(self, chat_id: int):
        await self.mute_stream(chat_id)

    async def pause_stream(self, chat_id: int):
        await self.pause_stream(chat_id)

    async def resume_stream(self, chat_id: int):
        await self.resume_stream(chat_id)

    async def unmute_stream(self, chat_id: int):
        await self.unmute_stream(chat_id)


call = MusicPlayer()