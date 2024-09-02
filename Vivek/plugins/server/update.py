import asyncio
import os
from datetime import datetime

import aiohttp
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import filters

from config import UPSTREAM_BRANCH
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
    response = await message.reply_text("Checking for available updates.....")
    try:
        repo = Repo()
    except GitCommandError:
        return await response.edit("Git commamd Error")
    except InvalidGitRepositoryError:
        return await response.edit("Invalid Git Respiratory")

    os.system(f"git fetch origin {UPSTREAM_BRANCH} &> /dev/null")
    await asyncio.sleep(7)

    verification = ""
    REPO_ = repo.remotes.origin.url.split(".git")[0]
    for checks in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}"):
        verification = str(checks.count())

    if verification == "":
        return await response.edit("Bot is Up To Date With Upstream Repo")

    updates = ""
    ordinal = lambda format: "%d%s" % (
        format,
        "tsnrhtdd"[(format // 10 % 10 != 1) * (format % 10 < 4) * format % 10 :: 4],
    )
    for info in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}"):
        updates += f"<b>➣ #{info.count()}: <a href={REPO_}/commit/{info}>{info.summary}</a> BY -> {info.author}</b>\n\t\t\t\t<b>➥ Commited On :</b> {ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} {datetime.fromtimestamp(info.committed_date).strftime('%b')}, {datetime.fromtimestamp(info.committed_date).strftime('%Y')}\n\n"

    _update_response_ = "<b>A New Upadte Is Available For The Bot !</b>\n\n➣ Pushing Upadtes Now \n\n<b><u>Upadtes:</u></b>\n\n"
    _final_updates_ = _update_response_ + updates

    if len(_final_updates_) > 4096:
        url = await paste(updates)
        await response.edit(
            f"<b>A New Upadte Is. Available For The Bot !</b>\n\n➣ Pushing Upadtes Now\n\n<u><b>Upadtes :</b></u>\n\n<a href={url}>Check Updates</a>"
        )
    else:
        await response.edit(_final_updates_, disable_web_page_preview=True)

    os.system("git stash &> /dev/null && git pull")

    os.system("pip3 install -r requirements.txt")
    await app.restart()
