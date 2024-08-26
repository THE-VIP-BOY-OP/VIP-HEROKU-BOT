from pyrogram import Client
from pyrogram.raw import base
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import GetGroupCall
from pyrogram.raw.types import InputGroupCall

from utils import filters


@Client.on_message(filters.command("vcmembers") & filters.sudo)
async def vc_members(client, message):
    msg = await message.reply_text("**Radhe Radhe**\nPlease wait...")

    full_chat: base.messages.ChatFull = await client.invoke(
        GetFullChannel(channel=(await client.resolve_peer(message.chat.id)))
    )

    if not full_chat.full_chat.call:
        return await msg.edit("**Radhe Radhe**\nOops, it looks like Voice chat is off")

    access_hash = full_chat.full_chat.call.access_hash
    ids = full_chat.full_chat.call.id
    input_group_call = InputGroupCall(id=ids, access_hash=access_hash)

    result = await client.invoke(GetGroupCall(call=input_group_call, limit=1))

    users = result.participants

    if not users:
        await msg.edit("**Radhe Radhe**\nThere are no members in the voice chat currently.")
        return

    mg = "**Radhe Radhe**\n\n"
    for user in users:
        title = None
        username = None
        if hasattr(user.peer, "channel_id") and user.peer.channel_id:
            user_id = -100 + user.peer.channel_id
            try:
                chat = await client.get_chat(user_id)
                title = chat.title
                username = chat.username or "Private Group"
            except Exception as e:
                chats = result.chats
                for c in chats:
                    if c.id == user.peer.channel_id:
                        title = c.title
        else:
            user_id = user.peer.user_id
            try:
                user_info = await client.get_users(user_id)
                title = user_info.mention
                username = user_info.username or "No Username"
            except Exception as e:
                for user_obj in result.users:
                    if user_obj.id == user_id:
                        username = user_obj.username or "No Username"
                        title = f"[{user_obj.first_name}](tg://user?id={user_id})"

        is_left = user.left
        just_joined = user.just_joined
        is_muted = True if user.muted and not user.can_self_unmute else False
        is_silent = True if user.muted and user.can_self_unmute else False

        mg += f"""**{'Title' if hasattr(user.peer, 'channel_id') and user.peer.channel_id else 'Name'}** = {title}
    **ID** : {user_id}"""
        if username:
            mg += f"\n    **Username** : {username}"

        mg += f"""
    **Is Lefted From Group** : {is_left}
    **Is Just Joined** : {just_joined}
    **Is Silent** : {is_silent}
    **Is Muted By Admin** : {is_muted}\n\n"""

    if mg != "**Radhe Radhe**\n":
        await msg.edit(mg)
    else:
        await msg.edit("**Radhe Radhe**\nNo members found.")