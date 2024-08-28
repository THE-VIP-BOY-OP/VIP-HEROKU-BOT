from pyrogram import Client
from pyrogram.enums import ChatType

from utils import filters

@Client.on_message(filters.command("vcmembers") & filters.sudo)
async def vc_members(client, message):
    msg = await message.reply_text("Fetching Participants please wait")
    try:
        async for m in client.get_call_members(message.chat.id):
            chat_id = m.chat.id
            username = m.chat.username
            is_hand_raised = m.is_hand_raised
            is_video_enabled = m.is_video_enabled
            is_left = m.is_left
            is_screen_sharing_enabled = m.is_screen_sharing_enabled
            is_muted = bool(m.is_muted and not m.can_self_unmute)
            is_speaking = not m.is_muted

            if m.chat.type != ChatType.PRIVATE:
                title = m.chat.title
            else:
                try:
                    title = (await client.get_users(chat_id)).mention
                except:
                    title = m.chat.first_name
        MS = '**Muted**' if is_muted else '**Speaking**'
        MSK = is_muted if is_muted else is_speaking
        TEXT = "**NAME: {0}**\n    **Username:** {1}\n    **Video Sharing:** {2}\n    **Screen Sharing:** {3}\n    **Is_hand_raised**: {4}\n    {5}: {6}\n    **Left The Group:** {7}".format(title, username, is_video_enabled, is_screen_sharing_enabled, is_hand_raised, MS, MSK, is_left)
        await msg.edit(TEXT or "No Participants in Voice Chat")
    except ValueError as e:
        await msg.edit(str(e))

