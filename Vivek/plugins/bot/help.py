import re
from math import ceil
from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Vivek import app
from Vivek.functions.help import SYMBOLS, BOT_HELP, BOT_CMD_MENU



COLUMN_SIZE = 4  # number of button height
NUM_COLUMNS = 3  # number of button width

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
                    callback_data="{}_module({},{})".format(
                        prefix, x.lower(), page_n
                    ),
                )
                for x in module_dict.keys()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x,
                    callback_data="{}_module({},{},{})".format(
                        prefix, chat, x.lower(), page_n
                    ),
                )
                for x in module_dict.keys()
            ]
        )

    pairs = [modules[i: i + NUM_COLUMNS] for i in range(0, len(modules), NUM_COLUMNS)]

    max_num_pages = ceil(len(pairs) / COLUMN_SIZE) if len(pairs) > 0 else 1
    modulo_page = page_n % max_num_pages

    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[modulo_page * COLUMN_SIZE: COLUMN_SIZE * (modulo_page + 1)] + [
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
async def help_button(client, query:):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back\((\d+)\)", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = "Click Below buttons for more info"

    if mod_match:
        module = mod_match.group(1)
        prev_page_num = int(mod_match.group(2))
        text = (
            f"<b><u>Here Is The Help For {module}:</u></b>\n"
            + BOT_HELP[module]["info"]
        )

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

        await query.message.edit(
            text=text,
            reply_markup=key,
            disable_web_page_preview=True,
        )

    elif home_match:
        await app.bot.send_message(
            query.from_user.id,
            text=top_text,
            reply_markup=paginate_modules(0, BOT_CMD_MENU, "help"),
            ),
        await query.message.delete()

    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=paginate_modules(curr_page, BOT_CMD_MENU, "help"),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=paginate_modules(next_page, BOT_CMD_MENU, "help"),
            disable_web_page_preview=True,
        )

    elif back_match:
        prev_page_num = int(back_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=  paginate_modules(prev_page_num, BOT_CMD_MENU, "help"),
            disable_web_page_preview=True,
        )

    elif create_match:
        keyboard = paginate_modules(0, BOT_CMD_MENU, "help")

        await query.message.edit(
            text=top_text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    await client.answer_callback_query(query.id)