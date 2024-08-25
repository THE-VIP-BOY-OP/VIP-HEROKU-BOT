from pyrogram import Client, filters 

@Client.on_message(filters.private & filters.text)
async def start(c,m):
    await m.reply_text(c.me.name)
