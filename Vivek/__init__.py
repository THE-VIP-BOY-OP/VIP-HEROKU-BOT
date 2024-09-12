import uvloop

uvloop.install()
from .core.client import app
from .functions.dir import dir
from .core.logger import LOGGER
from .functions.filters import edit_filters

dir()
edit_filters()
