import asyncio

from pyrogram import idle
from Vivek import app, bot, call

async def main():

    await app.start()
    await bot.start()
    await call.start()

    await idle()

    await app.stop()
    await bot.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())