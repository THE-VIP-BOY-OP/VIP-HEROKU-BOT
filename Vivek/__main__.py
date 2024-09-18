import asyncio
import atexit
import signal
import sys

from pyrogram import idle
from Vivek import app

loop = asyncio.get_event_loop_policy().get_event_loop()

async def run_shutdown():
    await app.stop()

def handle_signal(signal_number, frame):
    asyncio.ensure_future(run_shutdown())
    loop.stop()
    sys.exit(0)

def handle_exit():
    # Schedule shutdown asynchronously if event loop is running
    asyncio.ensure_future(run_shutdown())

async def main():
    atexit.register(handle_exit)
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGQUIT, handle_signal)
    await app.start()
    await idle()

if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    except Exception as e:
        # Use asyncio.ensure_future if loop is running
        if loop.is_running():
            asyncio.ensure_future(run_shutdown())
        else:
            loop.run_until_complete(run_shutdown())
        raise e
