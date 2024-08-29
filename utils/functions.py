from pyrogram import Client

class VClient(Client):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
