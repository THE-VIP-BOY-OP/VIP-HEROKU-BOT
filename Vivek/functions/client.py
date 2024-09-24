import os
import sys

from pyrogram import Client

from .help import BotHelp


class VClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help = BotHelp
        self.id = self.me.id
        self.username = self.me.username
        self.mention = self.me.mention
        self.first_name = self.me.first_name
        self.last_name = self.me.last_name
        self.name = (
            self.first_name + self.last_name if self.last_name else self.first_name
        )

    async def restart_script(self):
        os.execvp(sys.executable, [sys.executable, "-m", "Vivek", *sys.argv[1:]])
