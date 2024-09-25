import sys

from pyrogram import filters

from Vivek import FUNCTIONS, app


@app.on_message(filters.command("listloaded") & filters.sudo)
async def list_all_modules(client, message):
    all_funcs = FUNCTIONS["MODULES"]
    this_func = sys._getframe().f_code
    if this_func in all_funcs:
        all_funcs.remove(this_func)
    msg = await message.reply_text("Getting all loaded modules function")
    count = 0
    text = ""
    for func in all_funcs:
        count += 1
        text += f"{count} `{func.__name__}`\n"
    if text != "":
        await msg.edit(text)
