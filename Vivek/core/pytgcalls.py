from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

from .clients import app


class MusicPlayer(PyTgCalls):
    def __init__(self):
        super().__init__(app)

    async def play(self, file_path: str, chat_id: int):
        await self.play(chat_id, MediaStream(file_path))

    async def leave_call(self, chat_id: int):
        await self.leave_call(chat_id)

    async def mute_stream(self, chat_id: int):
        await self.mute_stream(chat_id)

    async def pause_stream(self, chat_id: int):
        await self.pause_stream(chat_id)

    async def resume_stream(self, chat_id: int):
        await self.resume_stream(chat_id)

    async def unmute_stream(self, chat_id: int):
        await self.unmute_stream(chat_id)


call = MusicPlayer()
