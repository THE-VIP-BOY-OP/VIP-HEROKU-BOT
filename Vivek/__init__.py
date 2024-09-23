import uvloop

# Applying uvloop event loop policy

uvloop.install()

# Logger 
from .functions.logger import LOGGER

# functions for editing pyrogram filters or for removing media's on starting

from .functions import edit_filters, dir

import asyncio
import importlib
from typing import Awaitable, Callable

import pyromod.listen  # noqa
from pyrogram import __version__ as v #noqa
from pyrogram import idle #noqa

from config import API_HASH, API_ID, BOT_TOKEN, LOG_GROUP_ID, STRING_SESSION #noqa
from Vivek.functions.client import VClient
from Vivek.plugins import ALL_MODULES #noqa

from .logger import LOGGER


dir()
edit_filters()

app = 