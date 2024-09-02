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


call = MusicPlayer()
