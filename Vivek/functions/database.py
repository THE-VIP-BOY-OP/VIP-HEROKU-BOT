import aiosqlite


class DB:
    def __init__(self, db_name: str):
        self.db_name = db_name

    async def _connect(self):
        return await aiosqlite.connect(self.db_name)

    async def create_table(self, table_name: str):
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

    async def save_my_data(self, table_name: str = "my_info", **kwargs):
        async with await self._connect() as db:
            data = str(kwargs)
            await db.execute(
                f"""
                INSERT INTO {table_name} (my_info) VALUES (?)
            """,
                (data,),
            )
            await db.commit()

    async def get_my_data(self, table_name: str = "my_info"):
        async with await self._connect() as db:
            async with db.execute(f"SELECT * FROM {table_name}") as cursor:
                rows = await cursor.fetchall()
                result = [{"id": row[0], **eval(row[1])} for row in rows]
                return result
