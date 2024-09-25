import os
import sys
from typing import Callable, Optional
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.filters import Filter

from .help import BotHelp


class VClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help = BotHelp()

    async def restart_script(self):
        """Restarts the script by executing the current Python file."""
        os.execvp(sys.executable, [sys.executable, "-m", "Vivek", *sys.argv[1:]])

    # pyrogram on_message decorator but adding handler, group in func.handlers without checking that it is Pyrogram.Client
    def on_message(
        self,
        filters: Optional[Filter] = None,
        group: int = 0,
    ) -> Callable:

        def decorator(func: Callable) -> Callable:
            handler = MessageHandler(func, filters)

            self.add_handler(handler, group)
            if not hasattr(func, "handlers"):
                func.handlers = []
            
            func.handlers.append((handler, group))

            return func

        return decorator