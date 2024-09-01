import uvloop

uvloop.install()

from Vivek.utils.filters import edit_filters
from Vivek.core.clients import call, bot, app
from .logging import LOGGER

HELPABLE = {}
edit_filters()
