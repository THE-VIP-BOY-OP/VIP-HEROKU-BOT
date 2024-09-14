from pyrogram import filters

from Vivek import app


@app.bot.on_message(filters.command(["start"]) & filters.private)
@LanguageStart
async def start_comm(client, message):
    if len(message.text.split()) > 1:
        dec_fileid = message.text.split(None, 1)[1]
        await message.reply_text(dec_fileid)
