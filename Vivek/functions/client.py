import os
import sys

from pyrogram import Client
from config import DATABASE_CHANNEL_ID
import os
from pyrogram.enums import MessagesFilter, MessageMediaType
from .help import BotHelp


class VClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help = BotHelp

    async def restart_script(self):
        os.execvp(sys.executable, [sys.executable, "-m", "Vivek", *sys.argv[1:]])


    

    async def load_database():
        messages = []
    
        async for message in self.search_messages(DATABASE_CHANNEL_ID, filter=MessagesFilter.PINNED):
            if message.media == MessageMediaType.DOCUMENT:
                if message.caption and "DATABASE" in message.caption:
                    if message.document.file_name.endswith(".db"):
                        messages.append(message)
    
        if len(messages) == 0:
            return False
    
        msg = messages[0]

        if os.path.isfile(".mydatabase.db"):
            try:
                os.remove(".mydatabase.db")
            except:
                pass

        root_directory = os.getcwd()
        file_path = os.path.join(root_directory, ".mydatabase.db")

        await msg.download(file_name=file_path)

        return os.path.isfile(".mydatabase.db")
                    
