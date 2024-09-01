from loguru import logger
import sys
import time

logger.remove()

def clt(seconds: int):
    return f"{seconds} seconds"

def setup_logger(exp: int):
    logger.add(
        "log.txt",
        rotation="5 MB", retention=clt(exp),
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} - {message}",
    )

logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "<cyan>{name}</cyan> - <level>{message}</level>",
)

logger.level("ERROR", color="<red>")
logger.disable("pyrogram")
logger.disable("httpx")

def LOGGER(name: str, exp: int = 864000):

    setup_logger(exp)
    return logger.bind(name=name)