from pyrogram.raw import base
from pyrogram.raw.functions.channels import GetFullChannel

from pyrogram import Client
from pyrogram.raw.functions.phone import GetGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel

from utils import filters

@Client.on_message(filters.command("vcmembers") & filters.sudo)
async def vc_members(client, message):
    full_chat: base.messages.ChatFull = await client.invoke(
            GetFullChannel(
                channel=(
                    await client.resolve_peer(message.chat.id)
                )
            )
    )
        

    access_hash = full_chat.full_chat.call.access_hash
    ids = full_chat.full_chat.call.id
    input_group_call = InputGroupCall(id=ids, access_hash=access_hash)
        

    result = await client.invoke(GetGroupCall(
            call=input_group_call,
            limit=1
        ))
        
    users =  result.participants
    msg = await message.reply_text("please wait")
    if not users:
        await msg.edit("There Are no memebers in voice chat currently")
        mg = ""
    for user in users:
    	if user.channel_id:
    	    user_id = -100 + user.channel_id
    	    title = (await client.get_chat(user_id)).title
            username = (await client.get_chat(user_id)).username or "Private Group"
        if user.peer:
            user_id = user.peer.user_id
            name = (await client.get_users(user_id)).mention or "Unknown"
            username = (await client.get_users(user_id)).mention or "No User Name"
        is_left = user.left
        just_joined= user.just_joined
        is_muted = True if user.muted and not user.can_self_unmute else False
        mg += f""" {'Title' if  user.channel_id else 'Name'} = {title if user.channel_id else name}
            id= {user_id}
            username = {username}
            is lefted = {is_left}
            is_just_joined = {just_joined}
            is_muted = {is_muted}"""
            
    await message.reply_text(mg)
        