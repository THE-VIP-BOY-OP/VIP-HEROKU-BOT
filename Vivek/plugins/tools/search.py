from pyrogram import filters
from youtubesearchpython.__future__ import VideosSearch

from Vivek import app

@app.on_message(filters.command(["search"]))
async def ytsearch(client, message):
    m = await message.reply_text("🔍 Searching on YouTube...")
    try:
        if len(message.command) < 2:
            return await m.edit_text(
                "❗ Provide a song/video name to search on YouTube."
            )
        query = message.text.split(None, 1)[1]
        results = VideosSearch(query, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            channel = result["channel"]["name"]
            views = result["viewCount"]["short"]
            upload_date = result["publishedTime"]

        text = (
            f"**🎵 Title**: [{title}](https://www.youtube.com/watch?v={vidid})\n"
            f"**⏱ Duration**: {duration_min}\n"
            f"**📅 Uploaded**: {upload_date}\n"
            f"**👁 Views**: {views}\n"
            f"**📺 Channel**: {channel}\n"
            f"**🔗 [Watch on YouTube](https://www.youtube.com/watch?v={vidid})**"
        )
        
        await m.edit_text(
            text=text,
            disable_web_page_preview=True,
        )
    except Exception as e:
        await m.edit_text(f"⚠️ An error occurred: {str(e)}")

app.help("Youtube").info("Searches YouTube for a video and provides details like title, views.").add("search", "Provide a <query> to search for videos or songs on YouTube.").done()