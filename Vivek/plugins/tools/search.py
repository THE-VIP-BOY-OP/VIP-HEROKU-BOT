from pyrogram import filters
from youtubesearchpython.__future__ import VideosSearch

from Vivek import app


@app.on_message(filters.command(["search"]))
async def ytsearch(client, message):
    m = await message.reply_text("Searching....")
    try:
        if len(message.command) < 2:
            return await m.edit_text("Provide A Song/Video Name To Search In Youtube")
        query = message.text.split(None, 1)[1]
        results = VideosSearch(query, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
        text = f"**Title** : {title}\n**Duration**: {duration_min}\n**Thumbnail**: {thumbnail}\n**Link**: https://www.youtube.com/watch?v={vidid}"
        await m.edit_text(
            text=text,
            disable_web_page_preview=True,
        )
    except Exception as e:
        await m.edit_text(str(e))
