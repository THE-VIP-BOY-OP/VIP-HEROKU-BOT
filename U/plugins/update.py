import os
import sys
from git import Repo
from os import system, execle, environ
from git.exc import InvalidGitRepositoryError
from pyrogram.types import Message
from pyrogram import filters, Client
from config import UPSTREAM_REPO, UPSTREAM_BRANCH, GIT_TOKEN, OWNER_ID

if GIT_TOKEN:
    GIT_USERNAME = UPSTREAM_REPO.split("com/")[1].split("/")[0]
    TEMP_REPO = UPSTREAM_REPO.split("https://")[1]
    UPSTREAM_REPO = f"https://{GIT_USERNAME}:{GIT_TOKEN}@{TEMP_REPO}"

else:
    UPSTREAM_REPO = UPSTREAM_REPO

def gen_chlog(repo, diff):
    upstream_repo_url = Repo().remotes[0].config_reader.get("url").replace(".git", "")
    ac_br = repo.active_branch.name
    ch_log = ""
    tldr_log = ""
    ch = f"<b>Updates for <a href={upstream_repo_url}/tree/{ac_br}>[{ac_br}]</a>:</b>"
    ch_tl = f"Updates for {ac_br}:"
    d_form = "%d/%m/%y || %H:%M"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"\n\n💬 <b>{c.count()}</b> 🗓 <b>[{c.committed_datetime.strftime(d_form)}]</b>\n<b>"
            f"<a href={upstream_repo_url.rstrip('/')}/commit/{c}>[{c.summary}]</a></b> 👨‍💻 <code>{c.author}</code>"
        )
        tldr_log += f"\n\n💬 {c.count()} 🗓 [{c.committed_datetime.strftime(d_form)}]\n[{c.summary}] 👨‍💻 {c.author}"
    if ch_log:
        return str(ch + ch_log), str(ch_tl + tldr_log)
    return ch_log, tldr_log


def updater():
    try:
        repo = Repo()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", UPSTREAM_REPO)
        origin.fetch()
        repo.create_head("UPSTREAM_BRANCH", origin.refs.UPSTREAM_BRANCH)
        repo.heads.UPSTREAM_BRANCH.set_tracking_branch(origin.refs.UPSTREAM_BRANCH)
        repo.heads.UPSTREAM_BRANCH.checkout(True)
    ac_br = repo.active_branch.name
    if "upstream" in repo.remotes:
        ups_rem = repo.remote("upstream")
    else:
        ups_rem = repo.create_remote("upstream", UPSTREAM_REPO)
    ups_rem.fetch(ac_br)
    changelog, tl_chnglog = gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    return bool(changelog), changelog, tl_chnglog


@Client.on_message(filters.command(["update", "up"]) & filters.user(OWNER_ID))
async def update_bot(_, message: Message):
    chat_id = message.chat.id
    msg = await message.reply_text("**🥀 Checking updates ✨...**")
    update_avail, changelog, _ = updater()
    if update_avail:
        await msg.edit("**🥀 Updates found! Pulling changes... ✨ ...**")
        os.system("git pull -f && pip3 install -U -r requirements.txt")
        await msg.edit(f"**🥀 Updates pulled successfully! ✨ ...**\n\n{changelog}")
        return
    await msg.edit("**🥀 Already up to date. ✨ ...**")