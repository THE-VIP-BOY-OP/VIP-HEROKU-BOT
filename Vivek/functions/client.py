import os
from datetime import datetime

import httpx
import pytz
from pyrogram import Client
from pyrogram.enums import MessageMediaType, MessagesFilter

from config import BOT_TOKEN, DATABASE_CHANNEL_ID

from ..core.logger import LOGGER
from .help import BotHelp

_msg = None

log = LOGGER(__name__)

import httpx
from config import BOT_TOKEN, LOG_GROUP_ID

def get_file_id():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    
    with open(".mydatabase.db", "rb") as file:
        files = {"document": file}
        data = {"chat_id": LOG_GROUP_ID}
        
        response = httpx.post(url, data=data, files=files)
        
        if response.status_code == 200:
            result = response.json()
            if result["ok"]:
                file_id = result["result"]["document"]["file_id"]
                return file_id
        else:
            return None


class VClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help = BotHelp

    async def restart_script(self):
        # os.execvp(sys.executable, [sys.executable, "-m", "Vivek", *sys.argv[1:]])
        os.system(f"kill -9 {os.getpid()} && python3 -m YukkiMusic")

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

    def export_database(self):
        global _msg
        if os.path.isfile(".mydatabase.db"):
            time = datetime.now(pytz.timezone("Asia/Kolkata")).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            caption = f"> this is DATABASE of {self.me.mention} Please don't Delete or Unpin This message\n> Else your bot data will be deleted\n Refreshed at {time}"

            new_media = {"type": "document", "media": get_file_id()}

            url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageMedia"

            data = {
                "chat_id": DATABASE_CHANNEL_ID,
                "message_id": _msg.id,
                "media": new_media,
                "caption": caption,
                "parse_mode": "Markdown",
            }
            with httpx.Client() as client:
                response = client.post(url, json=data)
