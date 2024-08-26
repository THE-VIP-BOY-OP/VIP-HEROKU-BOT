import re
from typing import List, Union, Pattern
from pyrogram import Client, filters, enums
from pyrogram.filters import create
from pyrogram.types import Message, Update, CallbackQuery, InlineQuery, PreCheckoutQuery
from config import PREFIX


class CustomFilters:

    reaction = staticmethod(create(lambda _, __, m: bool(m.reactions), "ReactionFilter"))
    admin = staticmethod(create(lambda _, __, m: bool(m.chat and m.chat.is_admin), "AdminFilter"))
    mentions = staticmethod(create(lambda _, __, m: bool(m.chat and m.mentioned)))
    private = staticmethod(create(lambda _, __, m: bool(m.chat and m.chat.type in {enums.ChatType.PRIVATE, enums.ChatType.BOT})))
    group = staticmethod(create(lambda _, __, m: bool(m.chat and m.chat.type in {enums.ChatType.GROUP, enums.ChatType.SUPERGROUP})))
    reply = staticmethod(create(lambda _, __, m: bool(m.reply_to_message_id or m.reply_to_story_id)))
    text = staticmethod(create(lambda _, __, m: bool(m.text)))
    me = staticmethod(create(lambda _, __, m: bool(m.from_user and m.from_user.is_self or getattr(m, "outgoing", False))))
    sudo = staticmethod(create(lambda _, __, m: bool(m.from_user and m.from_user.id in OWNER_ID or m.from_user.is_self)))
  
    @staticmethod
    def command(commands: Union[str, List[str]], case_sensitive: bool = False):
        command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")
      
        async def func(flt, client: Client, message: Message):
            username = client.me.username or ""
            text = message.text or message.caption
            message.command = None

            if not text:
                return False

            for prefix in PREFIX:
                if not text.startswith(prefix):
                    continue

                without_prefix = text[len(prefix):]

                for cmd in flt.commands:
                    if not re.match(
                        f"^(?:{cmd}(?:@?{username})?)(?:\s|$)",
                        without_prefix,
                        flags=0 if flt.case_sensitive else re.IGNORECASE,
                    ):
                        continue

                    without_command = re.sub(
                        f"{cmd}(?:@?{username})?\s?",
                        "",
                        without_prefix,
                        count=1,
                        flags=0 if flt.case_sensitive else re.IGNORECASE,
                    )

                    message.command = [cmd] + [
                        re.sub(r"\[\"'])", r"\1", m.group(2) or m.group(3) or "")
                        for m in command_re.finditer(without_command)
                    ]

                    return True

            return False

        commands = commands if isinstance(commands, list) else [commands]
        commands = {c if case_sensitive else c.lower() for c in commands}

        return create(func, "CommandFilter", commands=commands, case_sensitive=case_sensitive)
    @staticmethod
    def regex(pattern: Union[str, Pattern], flags: int = 0):
        """Filter updates that match a given regular expression pattern."""
        async def func(flt, _, update: Update):
            if isinstance(update, Message):
                value = update.text or update.caption
            elif isinstance(update, CallbackQuery):
                value = update.data
            elif isinstance(update, InlineQuery):
                value = update.query
            elif isinstance(update, PreCheckoutQuery):
                value = update.invoice_payload
            else:
                raise ValueError(f"Regex filter doesn't work with {type(update)}")

            if value:
                update.matches = list(flt.p.finditer(value)) or None

            return bool(update.matches)

        return create(
            func,
            "RegexFilter",
            p=pattern if isinstance(pattern, Pattern) else re.compile(pattern, flags)
          )
    
