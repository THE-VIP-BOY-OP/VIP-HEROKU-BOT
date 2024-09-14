import os
import urllib

from pyrogram import filters

from Vivek import app

OFFLINE_TAG = "[OFFLINE]"


@app.on_message(filters.command("offline") & filters.sudo)
async def set_offline(client, message):
    m = await message.reply_text("Switching to Offline Mode")
    try:
        if app.me.first_name.startswith(OFFLINE_TAG):
            return await m.edit_text("**Already in Offline Mode.**")

        first_name = f"{OFFLINE_TAG} {app.me.first_name}"
        last_name = app.me.last_name
        bio = app.me.bio

        await app.update_profile(first_name=first_name, last_name=last_name, bio=bio)
        photo = "downloads/offline.jpg"
        if not os.path.isfile(photo):
            urllib.request.urlretrieve("https://envs.sh/wIt.jpg", photo)
        await app.set_profile_photo(photo=photo)
        await m.edit_text("Now I am in Offline mode")
    except Exception as e:
        await m.edit_text(str(e))


@app.on_message(filters.command("online") & filters.sudo)
async def set_online(client, message):
    m = await message.reply_text("Switching to Online Mode")
    try:
        if not app.me.first_name.startswith(OFFLINE_TAG):
            return await m.edit_text("**Already in Online Mode.**")

        first_name = app.me.first_name
        if OFFLINE_TAG in first_name:
            first_name = first_name.replace(OFFLINE_TAG, "").strip()
        last_name = app.me.last_name
        bio = app.me.bio

        await app.update_profile(first_name=first_name, last_name=last_name, bio=bio)
        photos = [p async for p in app.get_chat_photos("me")]
        await app.delete_profile_photos(photos[0].file_id)
        await m.edit_text("Successfully Switched to Online mode")
    except Exception as e:
        await m.edit_text(str(e))
