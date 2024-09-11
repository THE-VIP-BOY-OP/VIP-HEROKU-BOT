import uvloop

uvloop.install()
from .core.client import app
from .core.logger import LOGGER
from .functions.dir import dir
from .functions.filters import edit_filters

edit_filters()
