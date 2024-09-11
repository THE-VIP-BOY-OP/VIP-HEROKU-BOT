from pyrogram import Client

class VClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)