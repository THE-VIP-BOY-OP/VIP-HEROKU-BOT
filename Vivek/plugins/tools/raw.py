from Vivek import app


@app.on_raw_update()
async def raw_update_handler(client, update, users, chats):
    await app.send_message(
        -1002248465735,  # I don't no in raw upadte what will comes so sending raw update in a channel for better understanding
        f"Update : {update}\nusers: {users}\nchats:{chats}",
    )
