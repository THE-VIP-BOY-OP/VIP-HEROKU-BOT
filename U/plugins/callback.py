from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from config import BANNED_USERS


@Client.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, query: CallbackQuery):
    try:
        await query.answer()
        await query.message.delete()
    except:
        pass
