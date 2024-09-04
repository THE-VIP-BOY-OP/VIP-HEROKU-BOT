import uvloop

uvloop.install()

import logging
import os
import sys
import shutil
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
        or file.endswith(".m4a")
        or file.endswith(".mp4")
        or file.endswith(".webm")
        or file.endswith(".png")
        or file.endswith(".session")
        or file.endswith(".session-journal")
    ):
        os.remove(file)

if "downloads" in listdir():
    shutil.rmtree("downloads")
    mkdir("downloads")
