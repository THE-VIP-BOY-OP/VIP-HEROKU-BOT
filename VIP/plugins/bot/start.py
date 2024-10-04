from pyrogram import filters

from VIP import app


@app.on_message(filters.command(["start"]))
async def start(client, message):
    await message.reply_text(
        f"Hello there! I am heroku control bot\n\nCheck hosted apps: /myhost, /heroku."
    )
