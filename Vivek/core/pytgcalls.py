from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

from .clients import appp


class MusicPlayer(PyTgCalls):
    def __init__(self):
        super().__init__(appp)

    async def play(self, file_path: str, chat_id: int):
        await self.play(chat_id, MediaStream(file_path))

    async def leave_call(self, chat_id: int):
        await self.leave_call(chat_id)


call = MusicPlayer()
