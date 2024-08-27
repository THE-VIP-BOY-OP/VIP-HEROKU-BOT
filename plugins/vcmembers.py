from pyrogram import Client
from pyrogram.enums import ChatType

from utils import filters

@Client.on_message(filters.command("vcmembers") & filters.sudo)
async def vc_members(client, message):
    msg = await message.reply_text("**Radhe Radhe**\nPlease wait...")
    TEXT = ""

    try:
        async for m in client.get_call_members(message.chat.id):
            chat_id = m.chat.id
            username = m.chat.username
            is_hand_raised = m.is_hand_raised
            is_video_enabled = m.is_video_enabled
            is_left = m.is_left
            is_screen_sharing_enabled = m.is_screen_sharing_enabled
            is_muted = bool(m.is_muted and not m.can_self_unmute)
            is_speaking = not is_muted

            if m.chat.type != ChatType.PRIVATE:
                title = m.chat.title
            else:
                try:
                    title = (await client.get_users(chat_id)).mention
                except:
                    title = m.chat.first_name

            TEXT += f"""**NAME: {title}**\n"""
            if username:
                TEXT += f"    USERNAME: @{username}\n"
            TEXT += f"""    VIDEO SHARING: {is_video_enabled}
    SCREEN SHARING: {is_screen_sharing_enabled}
    IS_HAND_RAISED: {is_hand_raised}
    {'MUTED' if is_muted else 'SPEAKING'}: {is_muted if is_muted else is_speaking}
    LEFT THE GROUP: {is_left}\n\n"""

        await msg.edit(TEXT or "No members found.")
    except ValueError as e:
        await msg.edit(str(e))
