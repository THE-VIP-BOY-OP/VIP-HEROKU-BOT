from motor.motor_asyncio import AsyncIOMotorClient
import json
import asyncio
import os
from bson import ObjectId
from pyrogram import filters
from pyrogram.errors import FloodWait
from Vivek import app

from pymongo.errors import OperationFailure
# Global variable
DB_NAME = "Yukki"  # Database that should not be deleted, only exported
MONGO_DB_URI = ""
SUDOERS = filters.sudo

# Custom JSON encoder to handle ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        return json.JSONEncoder.default(self, obj)

async def ex_port(db, db_name):
    """
    Exports the given MongoDB database to a .txt file in JSON format.
    :param db: The MongoDB database object.
    :param db_name: The name of the database to export.
    :return: The path of the exported file.
    """
    data = {}
    collections = await db.list_collection_names()

    for collection_name in collections:
        collection = db[collection_name]
        documents = await collection.find().to_list(length=None)
        data[collection_name] = documents
    
    backup_dir = "cache"
    os.makedirs(backup_dir, exist_ok=True)
    file_path = f"{backup_dir}/{db_name}_backup.txt"
    with open(file_path, "w") as backup_file:
        json.dump(data, backup_file, indent=4, cls=JSONEncoder)
    
    return file_path

async def drop_db(client, db_name):
    """
    Deletes the entire MongoDB database.
    """
    try:
        await client.drop_database(db_name)
    except OperationFailure:
    	pass

async def edit_or_reply(mystic, text):
    try:
        return await mystic.edit_text(text, disable_web_page_preview=True)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await mystic.edit_text(text, disable_web_page_preview=True)
    try:
        await mystic.delete()
    except:
        pass
    return await app.send_message(mystic.chat.id, disable_web_page_preview=True)

@app.on_message(filters.command("export") & SUDOERS)
async def export_database(client, message):
    mystic = await message.reply_text("Exporting Data from MongoDB...")
    _mongo_async_ = AsyncIOMotorClient(MONGO_DB_URI)
    databases = await _mongo_async_.list_database_names()

    for db_name in databases:
        if db_name == "admin":
            continue
        db = _mongo_async_[db_name]
        if db_name != DB_NAME:
            mystic = await edit_or_reply(mystic, f"Found data of {db_name} database. Uploading and deleting...")
            file_path = await ex_port(db, db_name)
            await app.send_document(message.chat.id, file_path, caption=f"MongoDB data of {db_name}")
            await drop_db(_mongo_async_, db_name)
            try:
                os.remove(file_path)
            except:
                pass
    
    db = _mongo_async_[DB_NAME]
    mystic = await edit_or_reply(mystic, f"Exporting the data of {app.mention}")
    
    async def progress(current, total):
        try:
            await mystic.edit_text(f"Downloaded {current * 100 / total:.1f}%")
        except:
            pass
    
    file_path = await ex_port(db, DB_NAME)
    await app.send_document(message.chat.id, file_path, caption=f"MongoDB backup of {app.mention}. You can import this into a new MongoDB instance by replying with /import", progress=progress)
    await mystic.delete()

@app.on_message(filters.command("import") & SUDOERS)
async def import_database(client, message):
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply_text("You need to reply to an export file to import it.")
    
    mystic = await message.reply_text("Downloading...")
    
    async def progress(current, total):
        try:
            await mystic.edit_text(f"Downloaded {current * 100 / total:.1f}%")
        except:
            pass
    
    file_path = await message.reply_to_message.download(progress=progress)
    
    try:
        with open(file_path, "r") as backup_file:
            data = json.load(backup_file)
    except (json.JSONDecodeError, IOError) as e:
        return await edit_or_reply(mystic, "Invalid exported data. Please provide a valid MongoDB export.")
    
    if not isinstance(data, dict):
        return await edit_or_reply(mystic, "Invalid data format. Please provide a valid MongoDB export.")
    
    _mongo_async_ = AsyncIOMotorClient(MONGO_DB_URI)
    databases = await _mongo_async_.list_database_names()
    
    if DB_NAME in databases:
        mystic = await edit_or_reply(mystic, "Existing data found. Deleting...")
        await drop_db(_mongo_async_, DB_NAME)
    
    db = _mongo_async_[DB_NAME]
    
    try:
        for collection_name, documents in data.items():
            mystic = await edit_or_reply(mystic, f"Importing collection {collection_name}...")
            collection = db[collection_name]
            if documents:
                await collection.insert_many(documents)
        await edit_or_reply(mystic, "Data successfully imported.")
    except Exception as e:
        await edit_or_reply(mystic, f"Error during import: {e}. Rolling back changes.")
        await drop_db(_mongo_async_, DB_NAME)
    
    try:
        os.remove(file_path)
    except:
        pass
