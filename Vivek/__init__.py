import uvloop

uvloop.install()
import os
import shutil
import sys

from .core.client import app
from .core.logger import LOGGER
from .functions.dir import dir
from .functions.filters import edit_filters

edit_filters()
