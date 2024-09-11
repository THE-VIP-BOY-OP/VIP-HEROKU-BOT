import asyncio

from Vivek import app


async def main():
    await app.start()


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
