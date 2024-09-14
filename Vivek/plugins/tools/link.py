import base64
from struct import pack

from pyrogram import enums, filters
from pyrogram.file_id import FileId

from Vivek import app


def unpack_new_file_id(new_file_id: str) -> str:

    decoded = FileId.decode(new_file_id)

    def encode_file_id(s: bytes) -> str:
        r = b""
        n = 0

        for i in s + bytes([22]) + bytes([4]):
            if i == 0:
                n += 1
            else:
                if n:
                    r += b"\x00" + bytes([n])
                    n = 0
                r += bytes([i])

        return base64.urlsafe_b64encode(r).decode().rstrip("=")

    file_id = encode_file_id(
        pack(
            "<iiqq",
            int(decoded.file_type),
            decoded.dc_id,
            decoded.media_id,
            decoded.access_hash,
        )
    )

    file_ref = base64.urlsafe_b64encode(decoded.file_reference).decode().rstrip("=")

    return file_ref


@app.on_message(filters.command(["link"]) & filters.sudo)
async def gen_link_s(client, message):
    replied = message.reply_to_message
    if not replied:
        return await message.reply("Reply to a message to get a shareable link.")
    file_type = replied.media
    if file_type not in [
        enums.MessageMediaType.PHOTO,
        enums.MessageMediaType.VOICE,
        enums.MessageMediaType.VIDEO_NOTE,
        enums.MessageMediaType.VIDEO,
        enums.MessageMediaType.AUDIO,
        enums.MessageMediaType.DOCUMENT,
    ]:
        return await message.reply("**Reply to a supported Media**")
    if message.has_protected_content:
        return await message.reply("The message is protected i cant store it")

    file_id = unpack_new_file_id((getattr(replied, file_type.value)).file_id)
    string = file_id
    outstr = base64.urlsafe_b64encode(string.encode("ascii")).decode().strip("=")
    user_id = message.from_user.id
    share_link = f"https://t.me/{app.bot.me.username}?start={outstr}"
    await message.reply(
        f"<b>⭕ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪɴᴋ:\n\n🔗 ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ :- {share_link}</b>",
        disable_web_page_preview=True,
    )
