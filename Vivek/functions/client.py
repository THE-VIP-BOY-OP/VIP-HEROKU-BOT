import os
import sys

from pyrogram import Client

from .help import BotHelp


class VClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help = BotHelp

    async def restart_script(self):
        os.execvp(sys.executable, [sys.executable, "-m", "Vivek", *sys.argv[1:]])
