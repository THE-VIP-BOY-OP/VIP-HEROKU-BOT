from pyrogram import Client, filters 

@Client.on_message(filters.private & filters.command("start"))
async def start(c,m):
    await m.reply_text("Radhe Radhe\n\nBot is now Under Development")
