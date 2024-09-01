from loguru import logger
import sys

logger.remove()

logger.add(
    "log.txt",
    rotation="5 MB",
    retention="10 files",
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


def LOGGER(name: str):
    return logger.bind(name=name)