from pyrogram import filters

from Vivek import FUNCTIONS, app


@app.on_message(filters.command("listloaded") & filters.sudo)
async def list_all_modules(client, message):
    all_funcs = FUNCTIONS["MODULES"]
    msg = await message.reply_text("Getting all loaded modules function")
    count = 0
    text = ""
    for func in all_funcs:
        if func.__name__ == str("list_all_modules") or func.__name__ == str("modules"):
            all_funcs.remove(func)
            continue
        count += 1
        text += f"{count} `{func.__name__}`\n"
    if text != "":
        await msg.edit(text)


@app.on_message(filters.command("unload") & filters.sudo)
async def modules(client, message):
    msg = await message.reply_text("Unloading....")
    user_input = " ".join(message.command[1:])
    if not user_input:
        return await msg.edit(
            "Provide a function name to unload it you can checkout all functions from loaded module by 'listloaded'"
        )
    for func in FUNCTIONS["MODULES"]:
        if user_input == func.__name__:
            handler = func.handlers
            for h in handler:
                app.remove_handler(*h)
            await msg.edit(f"Sucessfully unloaded {func.__name__}")
