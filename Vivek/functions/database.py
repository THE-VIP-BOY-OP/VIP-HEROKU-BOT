import json
import re

import aiosqlite


class DB:
    def __init__(self, db_name: str):
        self.db_name = db_name

    async def _connect(self):
        return await aiosqlite.connect(self.db_name)

    async def _initialize_table(self, table_name: str):
        if not re.match("^[A-Za-z_][A-Za-z0-9_]*$", table_name):
            raise ValueError(f"Invalid table name: {table_name}")
        async with await self._connect() as db:
            await db.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    my_info TEXT
                )
            """
            )
            await db.commit()

    async def save_my_data(self, table_name: str, **kwargs):
        await self._initialize_table(table_name)
        async with await self._connect() as db:
            await db.execute(f"DELETE FROM {table_name}")
            await db.commit()

            data = json.dumps(kwargs)
            await db.execute(
                f"""
                INSERT INTO {table_name} (my_info) VALUES (?)
            """,
                (data,),
            )
            await db.commit()

    async def get_my_data(self, table_name: str):
        await self._initialize_table(table_name)
        async with await self._connect() as db:
            async with db.execute(f"SELECT * FROM {table_name}") as cursor:
                row = await cursor.fetchone()
                if row:
                    result = {"id": row[0], **json.loads(row[1])}
                    return result
                return None


db = DB(".mydatabase.db")
