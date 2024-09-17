import asyncio
import atexit
import signal
import sys

from Vivek import app

loop = asyncio.get_event_loop_policy().get_event_loop()


def run_shutdown():
    asyncio.ensure_future(app.stop())


def handle_signal(signal_number, frame):
    run_shutdown()
    loop.stop()
    sys.exit(0)


def handle_exit():
    run_shutdown()


atexit.register(handle_exit)
signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGQUIT, handle_signal)


async def main():
    await app.start()
    await idle()


if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    except Exception:
        run_shutdown()
