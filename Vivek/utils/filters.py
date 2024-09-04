import re
from typing import List, Union

from pyrogram import Client, filters
from pyrogram.types import Message

from config import OWNER_ID, PREFIX


def edit_filters():

    filters.reaction = filters.create(
        lambda _, __, m: bool(m.reactions), "ReactionFilter"
    )

    filters.sudo = filters.create(
        lambda _, __, m: bool(
            m.from_user and (m.from_user.id in OWNER_ID or m.from_user.is_self)
        ),
        "SudoFilter",
    )

    def command(commands: Union[str, List[str]], case_sensitive: bool = False):
        command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

        async def func(flt, client: Client, message: Message):
            username = client.me.username or ""
            text = message.text or message.caption
            message.command = None

            if not text:
                return False

            for prefix in PREFIX:
                if prefix == "":
                    if not text.startswith(" "):
                        continue
                elif not text.startswith(prefix):
                    continue

                without_prefix = text[len(prefix):].lstrip()  # Remove prefix and leading spaces

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
                        re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                        for m in command_re.finditer(without_command)
                    ]

                    return True
            return False

        commands = commands if isinstance(commands, list) else [commands]
        commands = {c if case_sensitive else c.lower() for c in commands}

        return filters.create(
            func, "CommandFilter", commands=commands, case_sensitive=case_sensitive
        )

    filters.command = command