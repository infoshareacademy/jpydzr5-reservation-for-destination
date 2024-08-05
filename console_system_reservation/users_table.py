import sqlite3
from os import path


class UsersTable:
    database_name = "cinema_db.sqlite"

    @staticmethod
    def create_table(cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            "CREATE TABLE users ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "name VARCHAR(30) NOT NULL,"
            "surname VARCHAR(50) NOT NULL)"
        )

    @staticmethod
    def add_user(name: str, surname: str):
        if path.exists(UsersTable.database_name):
            connection = sqlite3.connect(UsersTable.database_name)
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (name, surname) VALUES (?, ?)", (name, surname)
            )
            connection.commit()
            connection.close()
