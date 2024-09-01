from pyrogram import Client

class Client(Client):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
