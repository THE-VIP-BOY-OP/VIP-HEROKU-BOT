import sys

from pyrogram import filters

from Vivek import FUNCTIONS, app


@app.on_message(filters.command("listloaded") & filters.sudo)
async def list_all_modules(client, message):
    this_func = sys._getframe().f_code
    if this_func in FUNCTIONS:
        FUNCTIONS.remove(this_func)
    await message.reply_text("Getting all loaded modules function")
    count = 0
    text = ""
    for func in FUNCTIONS:
        count += 1
        text += f"{count} `{func.__name__}`"
    if text != "":
        await message.reply_text(text)
