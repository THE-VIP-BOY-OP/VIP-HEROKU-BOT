import os
import sys

from pyrogram import Client


class VClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def restart():
        os.execvp(sys.executable, [sys.executable, "-m", "Vivek", *sys.argv[1:]])
