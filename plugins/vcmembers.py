from pyrogram import Client
from pyrogram.raw import base
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import GetGroupParticipants
from pyrogram.raw.types import InputGroupCall, InputPeerChat

from utils import filters
from config import LOG_GROUP_ID

@Client.on_message(filters.command("vcmembers") & filters.sudo)
async def vc_members(client, message):
    msg = await message.reply_text("**Radhe Radhe**\nPlease wait...")

    try:
        full_chat: base.messages.ChatFull = await client.invoke(
            GetFullChannel(channel=(await client.resolve_peer(message.chat.id)))
        )

        if not full_chat.full_chat.call:
            return await msg.edit("**Radhe Radhe**\nOops, it looks like Voice chat is off")

        access_hash = full_chat.full_chat.call.access_hash
        ids = full_chat.full_chat.call.id
        input_group_call = InputGroupCall(id=ids, access_hash=access_hash)
        input_peer_chat = InputPeerChat(chat_id=message.chat.id)

        result = await client.invoke(
            GetGroupParticipants(
                call=input_group_call,
                ids=[input_peer_chat],
                offset="",
                sources=[],
                limit=1000,
            )
        )

        users = result.participants

        if not users:
            return await msg.edit("**Radhe Radhe**\nThere are no members in the voice chat currently.")

        mg = "**Radhe Radhe**\n\n"
        for user in users:
            title, username = None, None
            if hasattr(user.peer, "channel_id") and user.peer.channel_id:
                user_id = -100 + user.peer.channel_id
                try:
                    chat = await client.get_chat(user_id)
                    title = chat.title
                    username = chat.username
                except Exception:
                    chats = result.chats
                    for c in chats:
                        if c.id == user.peer.channel_id:
                            title = c.title
            else:
                user_id = user.peer.user_id
                try:
                    user_info = await client.get_users(user_id)
                    title = user_info.mention
                    username = user_info.username
                except Exception:
                    for user_obj in result.users:
                        if user_obj.id == user_id:
                            username = user_obj.username or "No Username"
                            title = f"[{user_obj.first_name}](tg://user?id={user_id})"

            is_left = user.left
            just_joined = user.just_joined
            is_muted = bool(user.muted and not user.can_self_unmute)
            is_silent = bool(user.muted and user.can_self_unmute)

            mg += f"""**{'Title' if hasattr(user.peer, 'channel_id') and user.peer.channel_id else 'Name'}** = {title}
    **ID** : {user_id}"""
            if username:
                mg += f"\n    **Username** : {username}"

            mg += f"""
    **Is Left From Group** : {is_left}
    **Is Just Joined** : {just_joined}
    **Is Silent** : {is_silent}
    **Is Muted By Admin** : {is_muted}\n\n"""

        if mg != "**Radhe Radhe**\n\n":
            await msg.edit(mg)
        else:
            await msg.edit("**Radhe Radhe**\nNo members found.")

    except Exception as e:
        await client.send_message(LOG_GROUP_ID, f"An Error occured in vcmembers.py {e} ")
        await msg.edit(f"**Radhe Radhe**\nAn error occurred: {e}")