from pyrogram import Client

from Vivek.utils import filters


@Client.on_message(filters.command(["ping"]) & filters.sudo)
async def ping(client, message):
    await message.reply_text("I Am alive brooo")
