from pyrogram import Client

pause = {}


class VClient(Client):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)


async def is_music_playing(chat_id: int) -> bool:
    mode = pause.get(chat_id)
    if not mode:
        return False
    return mode


async def music_on(chat_id: int):
    pause[chat_id] = True


async def music_off(chat_id: int):
    pause[chat_id] = False
