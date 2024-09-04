from .logger import LOGGER
from Vivek.utils.filters import edit_filters
from Vivek.core.clients import app, bot
from os import listdir, mkdir
import sys
import os
import logging
import uvloop

uvloop.install()


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
