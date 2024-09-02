import uvloop

uvloop.install()

from Vivek.core.clients import app, bot
from Vivek.utils.filters import edit_filters

from .logger import LOGGER

HELPABLE = {}
edit_filters()
