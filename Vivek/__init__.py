from Vivek.core.clients import Vivek
from Vivek.core.pytgcall import pytgcall
from .logging import LOGGER
from Vivek.utils.filters import edit_filters

app = Vivek()
call = pytgcall()

edit_filters()
