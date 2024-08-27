from pyrogram.enums import ChatType
from pyrogram import Client
from utils import filters

@Client.on_message(filters.command("vcmembers") & filters.sudo)
async def vc_members(client, message):
    msg = await message.reply_text("**Radhe Radhe**\nPlease wait...")
    TEXT = ""

    try:
        async for m in client.get_call_members(message.chat.id):
            if m.chat.type != ChatType.PRIVATE:
                chat_id = m.chat.id
                title = m.chat.title
                username = m.chat.username
                bio = m.chat.bio
                is_hand_raised = m.is_hand_raised
                is_video_enabled = m.is_video_enabled
                is_left = m.is_left
                is_screen_sharing_enabled = m.is_screen_sharing_enabled
                is_muted = bool(m.is_muted and not m.can_self_unmute)
                is_silent = bool(m.is_muted and m.can_self_unmute)
            else:
                chat_id = m.chat.id
                try:
                    title = (await client.get_users(chat_id)).mention
                except:
                    title = m.chat.first_name
                username = m.chat.username
                bio = m.chat.bio
                is_hand_raised = m.is_hand_raised
                is_video_enabled = m.is_video_enabled
                is_left = m.is_left
                is_screen_sharing_enabled = m.is_screen_sharing_enabled
                is_muted = bool(m.is_muted and not m.can_self_unmute)
                is_silent = bool(m.is_muted and m.can_self_unmute)
            
            TEXT += f"""**NAME**: {title}\n"""
            if username:
                TEXT += f"    **USERNAME**: {username}"
            TEXT += f"""
    **BIO**: {bio}
    **VIDEO SHARING**: {is_video_enabled}
    **SCREEN SHARING**: {is_screen_sharing_enabled}
    **IS_HAND_RAISED**: {is_hand_raised}
    {'**MUTED**' if is_muted else '**SILENT**'}: {is_muted if is_muted else is_silent}
    **LEFTED FROM GROUP**: {is_left}\n\n"""
        
        await msg.edit(TEXT or "No members found.")

    except ValueError as e:
        await msg.edit(str(e))