import uvloop

uvloop.install()

import logging
import os
import sys
from os import listdir, mkdir

from Vivek.core.clients import app, bot
from Vivek.utils.filters import edit_filters

from .logger import LOGGER

HELPABLE = {}
edit_filters()

for file in os.listdir():
    if (
        file.endswith(".jpg")
        or file.endswith(".jpeg")
        or file.endswith(".mp3")
        or file.endswith(".png")
        or file.endswith(".session")
        or file.endswith(".session-journal")
    ):
        os.remove(file)

if "downloads" not in listdir():
    mkdir("downloads")
