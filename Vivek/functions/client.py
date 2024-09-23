import os
import sys
from typing import Union

from pyrogram import Client, enums
from pyrogram.session import Session
from pyrogram.storage import Storage

from .help import BotHelp


class VClient(Client):
    def __init__(
        self,
        name: str,
        api_id: Union[int, str] = None,
        api_hash: str = None,
        app_version: str = Client.APP_VERSION,
        device_model: str = Client.DEVICE_MODEL,
        system_version: str = Client.SYSTEM_VERSION,
        lang_code: str = Client.LANG_CODE,
        ipv6: bool = False,
        proxy: dict = None,
        test_mode: bool = False,
        bot_token: str = None,
        session_string: str = None,
        storage: Storage = None,
        in_memory: bool = None,
        phone_number: str = None,
        phone_code: str = None,
        password: str = None,
        workers: int = Client.WORKERS,
        workdir: str = Client.WORKDIR,
        plugins: dict = None,
        parse_mode: "enums.ParseMode" = enums.ParseMode.DEFAULT,
        no_updates: bool = None,
        takeout: bool = None,
        sleep_threshold: int = Session.SLEEP_THRESHOLD,
        hide_password: bool = False,
        max_concurrent_transmissions: int = Client.MAX_CONCURRENT_TRANSMISSIONS,
        huy: str = "huy",
    ):
        super().__init__(
            name=name,
            api_id=api_id,
            api_hash=api_hash,
            app_version=app_version,
            device_model=device_model,
            system_version=system_version,
            lang_code=lang_code,
            ipv6=ipv6,
            proxy=proxy,
            test_mode=test_mode,
            bot_token=bot_token,
            session_string=session_string,
            storage=storage,
            in_memory=in_memory,
            phone_number=phone_number,
            phone_code=phone_code,
            password=password,
            workers=workers,
            workdir=workdir,
            plugins=plugins,
            parse_mode=parse_mode,
            no_updates=no_updates,
            takeout=takeout,
            sleep_threshold=sleep_threshold,
            hide_password=hide_password,
            max_concurrent_transmissions=max_concurrent_transmissions,
        )
        self.help = BotHelp

    async def restart_script(self):
        os.execvp(sys.executable, [sys.executable, "-m", "Vivek", *sys.argv[1:]])
