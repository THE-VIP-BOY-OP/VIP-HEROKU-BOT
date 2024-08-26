from pyrogram import Client
from pyrogram.raw import base
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import GetGroupCall
from pyrogram.raw.types import InputGroupCall

from utils import filters


@Client.on_message(filters.command("vcmembers") & filters.sudo)
async def vc_members(client, message):
    full_chat: base.messages.ChatFull = await client.invoke(
        GetFullChannel(channel=(await client.resolve_peer(message.chat.id)))
    )

    access_hash = full_chat.full_chat.call.access_hash
    ids = full_chat.full_chat.call.id
    input_group_call = InputGroupCall(id=ids, access_hash=access_hash)

    result = await client.invoke(GetGroupCall(call=input_group_call, limit=1))

    users = result.participants
    msg = await message.reply_text("Please wait...")

    if not users:
        await msg.edit("There are no members in the voice chat currently.")
        return

    mg = ""
    for user in users:
        if user.peer.channel_id:
            user_id = -100 + user.channel_id
            chat = await client.get_chat(user_id)
            title = chat.title
            username = chat.username or "Private Group"
        else:
            user_id = user.peer.user_id
            user_info = await client.get_users(user_id)
            title = user_info.mention
            username = user_info.username or "No Username"

        is_left = user.left
        just_joined = user.just_joined
        is_muted = True if user.muted and not user.can_self_unmute else False

        mg += f""" {'Title' if user.channel_id else 'Name'} = {title}
        ID = {user_id}
        Username = {username}
        Is Left = {is_left}
        Just Joined = {just_joined}
        Is Muted = {is_muted}\n\n"""

    if mg:
        await msg.edit(mg)
    else:
        await msg.edit("No members found.")
