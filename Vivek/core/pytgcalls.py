from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

from .clients import app

call = PyTgCalls(app)


class MusicPlayer:
    
    @staticmethod
    def __getattr__(name):
        return getattr(call, name)

    @staticmethod
    async def play(file_path, chat_id):

        await call.play(
                    chat_id,
                    MediaStream(file_path)
        )


    @staticmethod
    async def leave_call(chat_id):
        await call.leave_call(chat_id)
