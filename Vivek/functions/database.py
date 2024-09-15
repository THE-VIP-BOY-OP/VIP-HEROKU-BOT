import json
import re
import sqlite3


class DB:
    def __init__(self, db_name: str):
        self.db_name = db_name

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _initialize_table(self, table_name: str):
        if not re.match("^[A-Za-z_][A-Za-z0-9_]*$", table_name):
            raise ValueError(f"Invalid table name: {table_name}")
        with self._connect() as db:
            db.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    my_info TEXT
                )
            """
            )
            db.commit()

    def save_my_data(self, table_name: str, **kwargs):
        self._initialize_table(table_name)
        with self._connect() as db:
            db.execute(f"DELETE FROM {table_name}")
            db.commit()

            data = json.dumps(kwargs)
            db.execute(
                f"""
                INSERT INTO {table_name} (my_info) VALUES (?)
            """,
                (data,),
            )
            db.commit()

    def get_my_data(self, table_name: str):
        self._initialize_table(table_name)
        with self._connect() as db:
            cursor = db.execute(f"SELECT * FROM {table_name}")
            row = cursor.fetchone()
            if row:
                result = {"id": row[0], **json.loads(row[1])}
                return result
            return None


db = DB(".mydatabase.db")
