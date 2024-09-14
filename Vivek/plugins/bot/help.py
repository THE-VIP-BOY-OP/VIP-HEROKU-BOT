import re
from math import ceil

from pyrogram import filters
from pyrogram.errors import BotInlineDisabled
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultPhoto,
)

from Vivek import LOGGER, app
from Vivek.functions.help import BOT_CMD_MENU, SYMBOLS

COLUMN_SIZE = 4  # number of button height
NUM_COLUMNS = 3  # number of button width

log = LOGGER(__name__)


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_modules(page_n, module_dict, prefix, chat=None, close: bool = False):
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x,
                    callback_data="{}_module({},{})".format(prefix, x, page_n),
                )
                for x in module_dict.keys()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x,
                    callback_data="{}_module({},{},{})".format(prefix, chat, x, page_n),
                )
                for x in module_dict.keys()
            ]
        )

    pairs = [modules[i : i + NUM_COLUMNS] for i in range(0, len(modules), NUM_COLUMNS)]

    max_num_pages = ceil(len(pairs) / COLUMN_SIZE) if len(pairs) > 0 else 1
    modulo_page = page_n % max_num_pages

    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[modulo_page * COLUMN_SIZE : COLUMN_SIZE * (modulo_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    SYMBOLS["arrow_left"],
                    callback_data="{}_prev({})".format(
                        prefix,
                        modulo_page - 1 if modulo_page > 0 else max_num_pages - 1,
                    ),
                ),
                EqInlineKeyboardButton(
                    SYMBOLS["close"] if close else SYMBOLS["back"],
                    callback_data="close" if close else "settingsback_helper",
                ),
                EqInlineKeyboardButton(
                    SYMBOLS["arrow_right"],
                    callback_data="{}_next({})".format(prefix, modulo_page + 1),
                ),
            )
        ]
    else:
        pairs.append(
            [
                EqInlineKeyboardButton(
                    SYMBOLS["close"] if close else SYMBOLS["back"],
                    callback_data="close" if close else "settingsback_helper",
                ),
            ]
        )

    return InlineKeyboardMarkup(pairs)


@app.bot.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query: InlineQuery):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back\((\d+)\)", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = "Click Below buttons for getting help about my Plugins"

    if mod_match:
        module = mod_match.group(1)
        prev_page_num = int(mod_match.group(2))
        text = BOT_CMD_MENU[module]

        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="↪️ Back", callback_data=f"help_back({prev_page_num})"
                    ),
                    InlineKeyboardButton(text="🔄 Close", callback_data="close"),
                ],
            ]
        )

        await app.bot.edit_inline_text(
            query.inline_message_id,
            text=text,
            reply_markup=key,
            disable_web_page_preview=True,
        )

    elif home_match:
        await app.bot.send_message(
            query.from_user.id,
            text=top_text,
            reply_markup=paginate_modules(0, BOT_CMD_MENU, "help"),
        )
        await query.message.delete()

    elif prev_match:
        curr_page = int(prev_match.group(1))
        await app.bot.edit_inline_text(
            query.inline_message_id,
            text=top_text,
            reply_markup=paginate_modules(curr_page, BOT_CMD_MENU, "help"),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await app.bot.edit_inline_text(
            query.inline_message_id,
            text=top_text,
            reply_markup=paginate_modules(next_page, BOT_CMD_MENU, "help"),
            disable_web_page_preview=True,
        )

    elif back_match:
        prev_page_num = int(back_match.group(1))
        await app.bot.edit_inline_text(
            query.inline_message_id,
            text=top_text,
            reply_markup=paginate_modules(prev_page_num, BOT_CMD_MENU, "help"),
            disable_web_page_preview=True,
        )

    elif create_match:
        keyboard = paginate_modules(0, BOT_CMD_MENU, "help")

        await app.bot.edit_inline_text(
            query.inline_message_id,
            text=top_text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    await client.answer_callback_query(query.id)


@app.on_message(filters.command("help") & filters.sudo)
async def help_(client, message):
    try:
        results = await app.get_inline_bot_results(
            app.bot.me.username, query="help_menu"
        )
        await message.reply_inline_bot_result(results.query_id, results.results[0].id)
    except BotInlineDisabled:
        await message.reply_text(
            "Please Turn on the InlineMode of the bot Then you will be able to use the bot"
        )


@app.bot.on_inline_query()
async def inline_query_handler(client, query):
    text = query.query.strip().lower()
    answers = []
    if text.strip() == "":
        return

    if text == "help_menu":
        photo = "https://te.legra.ph/file/4ec5ae4381dffb039b4ef.jpg"
        buttons = paginate_modules(0, BOT_CMD_MENU, "help")
        answers.append(
            InlineQueryResultPhoto(
                title="What do you think about my plugins",
                photo_url=photo,
                thumb_url=photo,
                caption="Click Below buttons for getting help about my Plugins",
                reply_markup=buttons,
            )
        )
        try:
            await app.bot.answer_inline_query(query.id, results=answers)
        except Exception as e:
            log.info(f"Error: {e}")
