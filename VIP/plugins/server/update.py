import asyncio
from datetime import datetime
from os import system as execute

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import filters
from urllib3 import disable_warnings, exceptions

from config import GIT_TOKEN, UPSTREAM_BRANCH, UPSTREAM_REPO
from VIP import ModuleHelp, app

disable_warnings(exceptions.InsecureRequestWarning)


@app.on_message(filters.command(["update", "gitpull", "up"]) & filters.sudo)
async def update_(client, message):
    response = await message.reply_text("Checking for available updates....")

    repo_link = UPSTREAM_REPO
    if GIT_TOKEN:
        git_username = repo_link.split("com/")[1].split("/")[0]
        temp_repo = repo_link.split("https://")[1]
        repo_link = f"https://{git_username}:{GIT_TOKEN}@{temp_repo}"

    try:
        repo = Repo()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("origin", repo_link)
        origin.fetch()
        repo.create_head(UPSTREAM_BRANCH, origin.refs[UPSTREAM_BRANCH])
        repo.heads[UPSTREAM_BRANCH].set_tracking_branch(origin.refs[UPSTREAM_BRANCH])
        repo.heads[UPSTREAM_BRANCH].checkout()
    except GitCommandError:
        return await response.edit("Git command error occurred.")

    repo.remote("origin").fetch(UPSTREAM_BRANCH)
    execute(f"git fetch origin {UPSTREAM_BRANCH} &> /dev/null")
    await asyncio.sleep(7)

    update_count = sum(1 for _ in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}"))

    if not update_count:
        return await response.edit("» Bot is up-to-date.")

    ordinal = lambda n: f"{n}{'tsnrhtdd'[(n//10%10!=1)*(n%10<4)*n%10::4]}"

    updates = "".join(
        f"<b>➣ #{info.count()}: <a href={repo.remotes.origin.url}/commit/{info}>{info.summary}</a> "
        f"By -> {info.author}</b>\n<b>➥ Commited On :</b> {ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} "
        f"{datetime.fromtimestamp(info.committed_date).strftime('%b, %Y')}\n\n"
        for info in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}")
    )

    if len(updates) > 4096:
        url = await Yukkibin(updates)
        await response.edit(
            f"**A new update is available for the bot**\n\n[Check Updates]({url})",
            disable_web_page_preview=True,
        )
    else:
        await response.edit(
            f"**A new update is available for the bot**\n\n{updates}",
            disable_web_page_preview=True,
        )

    execute("git stash &> /dev/null && git pull")
    execute("pip3 install --no-cache-dir -U -r requirements.txt")
    await app.restart_script()


help = ModuleHelp("server", "Server management plugin")
help.add(
    [
        "update",
        "Checks for and applies updates from the Git repository, then restarts the bot.",
    ]
)
