import asyncio
import os
from datetime import datetime

import aiohttp
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import filters

from config import GIT_TOKEN, UPSTREAM_BRANCH, UPSTREAM_REPO
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
        return await response.edit("Git command error")
    except InvalidGitRepositoryError:
        if UPSTREAM_REPO:
            repo_dir = os.getcwd()
            repo = Repo.init(repo_dir)
            origin = repo.create_remote("origin", UPSTREAM_REPO)
            origin.fetch()
            repo.create_head(UPSTREAM_BRANCH, origin.refs[UPSTREAM_BRANCH])
            repo.heads[UPSTREAM_BRANCH].set_tracking_branch(
                origin.refs[UPSTREAM_BRANCH]
            )
            repo.heads[UPSTREAM_BRANCH].checkout()
        else:
            return await response.edit(
                "Invalid Git repository and no UPSTREAM_REPO specified."
            )

    origin = repo.remotes.origin

    if GIT_TOKEN:
        repo_url_with_token = (
            f"https://{GIT_TOKEN}@{UPSTREAM_REPO.split('https://')[1]}"
        )
        origin.set_url(repo_url_with_token)

    os.system(f"git fetch origin {UPSTREAM_BRANCH} &> /dev/null")
    await asyncio.sleep(7)

    verification = ""
    REPO_ = repo.remotes.origin.url.split(".git")[0]
    for checks in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}"):
        verification = str(checks.count())

    if verification == "":
        return await response.edit("Bot is up to date with upstream repo")

    updates = ""
    ordinal = lambda format: "%d%s" % (
        format,
        "tsnrhtdd"[(format // 10 % 10 != 1) * (format % 10 < 4) * format % 10 :: 4],
    )
    for info in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}"):
        updates += f"<b>➣ #{info.count()}: <a href={REPO_}/commit/{info}>{info.summary}</a> BY -> {info.author}</b>\n\t\t\t\t<b>➥ Commited On :</b> {ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} {datetime.fromtimestamp(info.committed_date).strftime('%b')}, {datetime.fromtimestamp(info.committed_date).strftime('%Y')}\n\n"

    _update_response_ = "<b>A new update is available for the bot!</b>\n\n➣ Pushing updates now\n\n<b><u>Updates:</u></b>\n\n"
    _final_updates_ = _update_response_ + updates

    if len(_final_updates_) > 4096:
        url = await paste(updates)
        await response.edit(
            f"<b>A new update is available for the bot!</b>\n\n➣ Pushing updates now\n\n<u><b>Updates:</b></u>\n\n<a href={url}>Check Updates</a>"
        )
    else:
        await response.edit(_final_updates_, disable_web_page_preview=True)

    os.system(
        f"git stash &> /dev/null && git pull {repo_url_with_token} {UPSTREAM_BRANCH}"
    )

    os.system("pip3 install -r requirements.txt")
    await app.restart()
