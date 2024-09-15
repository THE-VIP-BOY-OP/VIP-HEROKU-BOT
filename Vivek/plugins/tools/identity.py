from pyrogram import filters
from Vivek import app
from Vivek.functions import db

@app.on_message(filters.command("clone") & filters.sudo)
async def set_offline(client, message):
	if not message.from_user.is_self:
	    if message.reply_to_message and message.reply_to_message.from_user:
	       m = await message.reply_text("Cloning Replied users details please wait...")
		   try:
		       user = await app.get_users(message.reply_to_message.from_user.id)
		        first_name = user.first_name
			    last_name = user.last_name
	    	    info = await app.get_chat(message.reply_to_message.from_user.id)
			    bio = info.bio
			    birth=info.birthday
			    photo = await app.download_media(info.photo.big_file_id)
				
			    my_name = app.me.first_name
			    my_s_name = app.me.last_name
			    minfo = await app.get_chat("self")
			    mbio = minfo.bio
		        mbirth = minfo.birthday
		        await db.save_my_data(
                        "my_info_table", 
                        first_name=my_name, 
                        last_name=my_s_name, 
                        bio=mbio,
                        birth=mbirth,
                        photo=minfo.photo.big_file_id,
                 )
                await app.update_profile(first_name=first_name, last_name=last_name, bio=bio)
                photos = [p async for p in app.get_chat_photos("me")]
                await app.delete_profile_photos([p.file_id for p in photos[0:]])
                await app.set_profile_photo(photo=photo)
                await app.update_birthday(day=birth.day, month=birth.month, year=birth.year)
                return await m.edit_text(f"Successfully cloned the details of {user.mention}")
            except Exception as e:
            	await m.edit_text(str(e))

        else:
        	m = await message.reply_text("Cloning Your details please wait...")
		   try:
		       user = await app.get_users(message.from_user.id)
		        first_name = user.first_name
			    last_name = user.last_name
	    	    info = await app.get_chat(message.from_user.id)
			    bio = info.bio
			    birth=info.birthday
			    photo = await app.download_media(info.photo.big_file_id)
				
			    my_name = app.me.first_name
			    my_s_name = app.me.last_name
			    minfo = await app.get_chat("self")
			    mbio = minfo.bio
		        mbirth = minfo.birthday
		        await db.save_my_data(
                        "my_info_table", 
                        first_name=my_name, 
                        last_name=my_s_name, 
                        bio=mbio,
                        birth=mbirth,
                        photo=minfo.photo.big_file_id,
                 )
                await app.update_profile(first_name=first_name, last_name=last_name, bio=bio)
                photos = [p async for p in app.get_chat_photos("me")]
                await app.delete_profile_photos([p.file_id for p in photos[0:]])
                await app.set_profile_photo(photo=photo)
                await app.update_birthday(day=birth.day, month=birth.month, year=birth.year)
                return await m.edit_text(f"Successfully cloned the details of {user.mention}")
            except Exception as e:
            	await m.edit_text(str(e))
    else:
    	await message.reply_text("Reply to user message to clone here details")
