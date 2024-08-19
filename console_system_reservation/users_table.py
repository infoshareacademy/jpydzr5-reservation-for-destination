import sqlite3
from os import path


class UsersTable:
    DATABASE_NAME = "cinema_db.sqlite"

    @staticmethod
    def create_table(cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            "CREATE TABLE cinema_user ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "name VARCHAR(30) NOT NULL,"
            "surname VARCHAR(50) NOT NULL)"
        )

    @staticmethod
    def add_user(name: str, surname: str):
        if path.exists(UsersTable.DATABASE_NAME):
            connection = sqlite3.connect(UsersTable.DATABASE_NAME)
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO cinema_user (name, surname) VALUES (?, ?)", (name, surname)
            )
            connection.commit()
            connection.close()
