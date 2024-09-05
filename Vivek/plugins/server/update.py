import os

import aiohttp
from pyrogram import filters

from Vivek import app

BASE = "https://batbin.me/"


async def post(url: str, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, **kwargs) as resp:
            try:
                data = await resp.json()
            except Exception:
                data = await resp.text()
        return data


async def paste(text):
    resp = await post(f"{BASE}api/v2/paste", data=text)
    if not resp["success"]:
        return
    link = BASE + resp["message"]
    return link


@app.on_message(filters.command(["update", "up", "gitpull"]) & filters.sudo)
async def update_(client, message):
    await message.reply_text("Updating...")
    os.system("git pull && bash start")
