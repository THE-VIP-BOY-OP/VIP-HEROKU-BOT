import os

from pyrogram import Client
from pyrogram.enums import MessageMediaType, MessagesFilter

from config import DATABASE_CHANNEL_ID

from .help import BotHelp

import sys

class VClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help = BotHelp

    async def restart_script(self):
        os.execvp(sys.executable, [sys.executable, "-m", "Vivek", *sys.argv[1:]])

    async def load_database(self):
        global _msg
        messages = []

        async for message in self.search_messages(
            DATABASE_CHANNEL_ID, filter=MessagesFilter.PINNED
        ):
            if message.media == MessageMediaType.DOCUMENT:
                if message.caption and "DATABASE" in message.caption:
                    if message.document.file_name.endswith(".db"):
                        messages.append(message)

        if len(messages) == 0:
            return False

        msg = max(messages, key=lambda msg: max(msg.date, msg.edit_date or msg.date))
        for message in messages:
            if message.id != msg.id:
                await self.delete_messages(DATABASE_CHANNEL_ID, message.id)

        if os.path.isfile(".mydatabase.db"):
            try:
                os.remove(".mydatabase.db")
            except:
                pass

        root_directory = os.getcwd()
        file_path = os.path.join(root_directory, ".mydatabase.db")

        _msg = msg
        await msg.download(file_name=file_path)

        return os.path.isfile(".mydatabase.db")
