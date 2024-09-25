import sys

from pyrogram import filters

from Vivek import FUNCTIONS, app


@app.on_message(filters.command("listloaded") & filters.sudo)
async def list_all_modules(client, message):
    all_funcs = FUNCTIONS["MODULES"]
    msg = await message.reply_text("Getting all loaded modules function")
    count = 0
    text = ""
    for func in all_funcs:
        if func.__name__ == sys._getframe().f_code.co_name:
            func.remove(sys._getframe().f_code.co_name)
            continue
        count += 1
        text += f"{count} `{func.__name__}`\n"
    if text != "":
        await msg.edit(text)
