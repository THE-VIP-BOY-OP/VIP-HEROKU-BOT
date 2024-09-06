import asyncio
import os
import random
from typing import Optional, Union

import httpx
import requests
from pyrogram import Client
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from config import LOG_GROUP_ID
from Vivek.logger import LOGGER

log = LOGGER(__name__)

S12KK = {}
pause = {}
mute = {}
active = []
chatlist = []


class VClient(Client):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)


class MelodyError(Exception):

    def __init__(self, message):
        super().__init__(message)


class DownloadError(Exception):

    def __init__(self, errr: str):
        super().__init__(errr)


def S12K(chat_id: Optional[int] = None):
    if chat_id is not None:
        S12KK[1234] = chat_id
    return S12KK.get(1234) or LOG_GROUP_ID


class Vivek:

    @staticmethod
    async def get_url(message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)

        text = ""
        offset = None
        length = None

        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url

        if offset is None:
            return None

        return text[offset : offset + length]

    @staticmethod
    async def track(link: str, randomize=False):
        if "&" in link:
            link = link.split("&")[0]

        limit = 10 if randomize else 1
        results = VideosSearch(link, limit=limit)
        result_data = await results.next()

        if not result_data["result"]:
            raise MelodyError("No results Found in Search")

        if randomize:
            index = random.randint(3, 9)
            result = result_data["result"][index]
        else:
            result = result_data["result"][0]

        title = result["title"]
        duration_min = result["duration"]
        vidid = result["id"]
        yturl = result["link"]
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]

        track_details = {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }
        return track_details

    @staticmethod
    async def run_shell_cmd(command):
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()
        return process.returncode, stdout.decode(), stderr.decode()

    @staticmethod
    async def download(vidid, video=False, retries=3):
        videoid = vidid
        url = f"https://invidious.jing.rocks/api/v1/videos/{videoid}"

        for attempt in range(retries):
            try:
                response = requests.get(url)
                video_data = response.json()

                formats = video_data.get("adaptiveFormats", [])
                if not formats:
                    raise MelodyError("No media formats found")

                if video:
                    video_url = None
                    video_path = os.path.join("downloads", f"{videoid}.mp4")

                    fmta = video_data.get("formatStreams", [])
                    for fmt in fmta:
                        video_url = fmt.get("url")
                        if video_url:
                            break

                    if video_url is None:
                        raise MelodyError("Video URL not found in requests")

                    cmd = f'yt-dlp -o "{video_path}" "{video_url}"'
                    returncode, stdout, stderr = await Vivek.run_shell_cmd(cmd)

                    if returncode != 0:
                        raise MelodyError(f"Video download failed with error: {stderr}")

                    return video_path
                else:
                    audio_url = None
                    audio_path = os.path.join("downloads", f"{videoid}.m4a")

                    for fmt in formats:
                        if fmt.get("audioQuality") == "AUDIO_QUALITY_MEDIUM":
                            audio_url = fmt.get("url")
                            break

                    if audio_url is None:
                        for fmt in formats:
                            if fmt.get("type") in ["audio/mp4", "audio/webm"]:
                                audio_url = fmt.get("url")
                                break

                    if audio_url is None:
                        raise MelodyError("Audio URL not found")

                    cmd = f'yt-dlp -o "{audio_path}" "{audio_url}"'
                    returncode, stdout, stderr = await Vivek.run_shell_cmd(cmd)

                    if returncode != 0:
                        raise MelodyError(f"Audio download failed with error: {stderr}")

                    return audio_path

            except (requests.RequestException, MelodyError) as e:
                if attempt + 1 == retries:
                    raise MelodyError(f"An error occurred after {retries} retries: {e}")
                await asyncio.sleep(2)

        raise MelodyError(f"Failed to download after {retries} attempts")

    @staticmethod
    async def get_download(vidid: str, video: bool = False):
        API = "https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }

        if video:
            path = os.path.join("downloads", f"{vidid}.mp4")
            data = {
                "url": f"https://www.youtube.com/watch?v={vidid}",
                "vQuality": "480",
            }
        else:
            path = os.path.join("downloads", f"{vidid}.m4a")
            data = {
                "url": f"https://www.youtube.com/watch?v={vidid}",
                "isAudioOnly": "True",
                "aFormat": "opus",
            }

        try:
            async with httpx.AsyncClient(http2=True) as client:
                response = await client.post(API, headers=headers, json=data)
                response.raise_for_status()

                results = response.json().get("url")
                if not results:
                    raise ValueError("No download URL found in the response")

                cmd = ["yt-dlp", results, "-o", path]
                returncode, stdout, stderr = await Vivek.run_shell_cmd(cmd)

                if returncode == 0 and os.path.isfile(path):
                    return path
                else:
                    raise DownloadError("Download failed or file not found.")

        except (
            httpx.RequestError,
            httpx.HTTPStatusError,
            ValueError,
            DownloadError,
        ) as e:
            try:
                path = await download(vidid, video)
                return path
            except MelodyError as fallback_error:
                raise DownloadError(
                    f"Download failed after fallback attempt: {str(fallback_error)}"
                )

    @staticmethod
    async def is_music_playing(chat_id: int) -> bool:
        return pause.get(chat_id, False)

    @staticmethod
    async def music_on(chat_id: int):
        pause[chat_id] = True

    @staticmethod
    async def music_off(chat_id: int):
        pause[chat_id] = False

    @staticmethod
    async def is_muted(chat_id: int) -> bool:
        return mute.get(chat_id, False)

    @staticmethod
    async def mute_on(chat_id: int):
        mute[chat_id] = True

    @staticmethod
    async def mute_off(chat_id: int):
        mute[chat_id] = False

    @staticmethod
    async def get_active_chats() -> list:
        return active

    @staticmethod
    async def is_active_chat(chat_id: int) -> bool:
        return chat_id in active

    @staticmethod
    async def add_active_chat(chat_id: int):
        if chat_id not in active:
            active.append(chat_id)

    @staticmethod
    async def remove_active_chat(chat_id: int):
        if chat_id in active:
            active.remove(chat_id)
