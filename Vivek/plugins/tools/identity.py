from pyrogram import filters

from Vivek import app
from Vivek.functions import db


@app.on_message(filters.command("clone") & filters.sudo)
async def clone_userinfo(client, message):
    if message.from_user.id != app.me.id:
        if message.reply_to_message and message.reply_to_message.from_user:
            m = await message.reply_text(
                "Cloning replied user's details, please wait..."
            )
            try:
                user = await app.get_users(message.reply_to_message.from_user.id)
                first_name = user.first_name
                last_name = user.last_name
                info = await app.get_chat(message.reply_to_message.from_user.id)
                bio = info.bio
                birth = info.birthday
                photo = info.photo

                if photo:
                    photo = await app.download_media(photo.big_file_id)
                else:
                    photo = None

                me = await app.get_me()
                minfo = await app.get_chat("me")
                mbio = minfo.bio
                mbirth = minfo.birthday
                minfo_photo = minfo.photo

                db.save_my_data(
                    "my_info_table",
                    first_name=me.first_name,
                    last_name=me.last_name,
                    bio=mbio,
                    birth_day=mbirth.day if mbirth else None,
                    birth_month=mbirth.month if mbirth else None,
                    birth_year=mbirth.year if mbirth else None,
                    photo=minfo_photo.big_file_id if minfo_photo else None,
                )

                await app.update_profile(
                    first_name=first_name, last_name=last_name, bio=bio
                )
                photos = [p async for p in app.get_chat_photos("me")]
                await app.delete_profile_photos([p.file_id for p in photos])
                if photo:
                    await app.set_profile_photo(photo=photo)
                if birth:
                    await app.update_birthday(
                        day=birth.day,
                        month=birth.month,
                        year=birth.year,
                    )

                return await m.edit_text(
                    f"Successfully cloned the details of {user.mention}"
                )

            except Exception as e:
                await m.edit_text(str(e))

        else:
            m = await message.reply_text("Cloning your details, please wait...")
            try:
                user = await app.get_users(message.from_user.id)
                first_name = user.first_name
                last_name = user.last_name
                info = await app.get_chat(message.from_user.id)
                bio = info.bio
                birth = info.birthday
                photo = info.photo

                if photo:
                    photo = await app.download_media(photo.big_file_id)
                else:
                    photo = None

                me = await app.get_me()
                minfo = await app.get_chat("me")
                mbio = minfo.bio
                mbirth = minfo.birthday
                minfo_photo = minfo.photo

                db.save_my_data(
                    "my_info_table",
                    first_name=me.first_name,
                    last_name=me.last_name,
                    bio=mbio,
                    birth_day=mbirth.day if mbirth else None,
                    birth_month=mbirth.month if mbirth else None,
                    birth_year=mbirth.year if mbirth else None,
                    photo=minfo_photo.big_file_id if minfo_photo else None,
                )

                await app.update_profile(
                    first_name=first_name, last_name=last_name, bio=bio
                )
                photos = [p async for p in app.get_chat_photos("me")]
                await app.delete_profile_photos([p.file_id for p in photos])
                if photo:
                    await app.set_profile_photo(photo=photo)
                if birth:
                    await app.update_birthday(
                        day=birth.day,
                        month=birth.month,
                        year=birth.year,
                    )

                return await m.edit_text(f"Successfully cloned your details")

            except Exception as e:
                await m.edit_text(str(e))
    else:
        await message.reply_text("Reply to a user's message to clone their details")
