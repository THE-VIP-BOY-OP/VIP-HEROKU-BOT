import asyncio
import os
from datetime import datetime

import pytz
from pyrogram.enums import MessageMediaType, MessagesFilter
from pyrogram.types import InputMediaDocument

from config import DATABASE_CHANNEL_ID
from Vivek import app


async def export_database():
    messages = []
    async for message in app.search_messages(
        DATABASE_CHANNEL_ID, filter=MessagesFilter.PINNED
    ):
        if message.media == MessageMediaType.DOCUMENT:
            if message.caption and "DATABASE" in message.caption:
                if message.document.file_name.endswith(".db"):
                    messages.append(message)

    if len(messages) == 0:
        return await app.send_document(DATABASE_CHANNEL_ID, ".mydatabase.db", caption="DATABASE")

    msg = max(messages, key=lambda msg: max(msg.date, msg.edit_date or msg.date))
    for message in messages:
        if message.id != msg.id:
            await app.delete_messages(DATABASE_CHANNEL_ID, message.id)

    if os.path.isfile(".mydatabase.db"):
        time = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")

        media = InputMediaDocument(
            media=".mydatabase.db",
            caption=(
                f"> this is DATABASE. Please don't Delete or Unpin This message\n"
                "> Else your bot data will be deleted\n"
                f"Refreshed at {time}"
            ),
        )
        await app.edit_message_media(
            chat_id=DATABASE_CHANNEL_ID,
            message_id=msg.id,
            media=media,
            file_name=".mydatabase.db",
        )


async def run_export_stop():
    while True:
        await export_database()
        await asyncio.sleep(3600)


asyncio.create_task(run_export_stop())
