from pyrogram import Client
from pyrogram.raw import base
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import GetGroupCall
from pyrogram.raw.types import InputGroupCall

from utils import filters


@Client.on_message(filters.command("vcmembers") & filters.sudo)
async def vc_members(client, message):
   msg = await message.reply_text("Please wait...")

    full_chat: base.messages.ChatFull = await client.invoke(
        GetFullChannel(channel=(await client.resolve_peer(message.chat.id)))
    )
    if not full_chat.full_chat.call:
        return await msg.edit("Radhe Radhe\nOops looks like Voice chat is off")
    access_hash = full_chat.full_chat.call.access_hash
    ids = full_chat.full_chat.call.id
    input_group_call = InputGroupCall(id=ids, access_hash=access_hash)

    result = await client.invoke(GetGroupCall(call=input_group_call, limit=1))

    users = result.participants
 
    if not users:
        await msg.edit("There are no members in the voice chat currently.")
        return

    mg = ""
    for user in users:
        if user.peer.channel_id:
            user_id = -100 + user.peer.channel_id
            try:
                chat = await client.get_chat(user_id)
                title = chat.title
                username = chat.username or "Private Group"
            except:
                chats = result.chats
                for c in chats:
                    if c.id == user.peer.channel_id:
                        title = c.title
                        username = "Can't Say"
        else:
            user_id = user.peer.user_id
           try:
                user_info = await client.get_users(user_id)
                title = user_info.mention
                username = user_info.username or "No Username"
           except:
               user_info = result.users
              for user in user_info:
                 if user.id == user_id:
                    username = user.username or "No Username"
                    title = [user.first_name](f"tg://user?id={user_id}")
        is_left = user.left
        just_joined = user.just_joined
        is_muted = True if user.muted and not user.can_self_unmute else False

        mg += f""" {'Title' if user.peer.channel_id else 'Name'} = {title}
ID = {user_id}
Username = {username}
Is Left = {is_left}
Just Joined = {just_joined}
Is Muted = {is_muted}\n\n"""

    if mg:
        await msg.edit(mg)
    else:
        await msg.edit("No members found.")
