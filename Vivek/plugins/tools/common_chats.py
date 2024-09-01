from Vivek import app
from pyrogram import filters
from pyrogram.errors import UsernameInvalid

@app.on_message(filters.sudo & filters.command(["common_chats"]))
async def get_common_chats(client, message):

    if len(message.command) < 2 or not message.reply_to_message:
        return await message.reply_text("Usage: /common_chats @username")
    if message.reply_to_message:
        username = message.reply_to_message.from_user.username if message.reply_to_message.from_user.username else message.reply_to_message.from_user.id

    if not message.reply_to_message:
        username = message.command[1]

    try:
        a = await app.get_common_chats(username)
    except UsernameInvalid:
        return await message.reply_text("The username is invalid. Please provide a valid username.")
    
    if not a:
        return await message.reply_text("No common chats found.")
    
    msg = "Found Some Common Chats:\n"
    for chat in a:
        title = chat.title
        chat_id = chat.id
        username = chat.username or "Private Group"
        members_count = chat.members_count or "Unknown"

        msg += f"Chat Name: {title}\n    ID: {chat_id}\n    Username: {username}\n    Members: {members_count}\n\n"
        
    if msg != "Found Some Common Chats:\n":
        await message.reply_text(msg)