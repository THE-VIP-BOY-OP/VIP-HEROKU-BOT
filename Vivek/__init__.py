import uvloop

uvloop.install()

from Vivek.core.clients import app, bot, call
from Vivek.utils.filters import edit_filters

from .logging import LOGGER

HELPABLE = {}
edit_filters()
