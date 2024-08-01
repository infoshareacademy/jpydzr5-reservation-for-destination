import sqlite3
from os import path


class UsersDB:
    @staticmethod
    def create_table(database_name="cinema_reservation_db.sqlite"):
        if not path.exists(database_name):
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()
            cursor.execute(
                "CREATE TABLE users ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "name VARCHAR(30) NOT NULL,"
                "surname VARCHAR(50) NOT NULL)"
            )
            connection.commit()
            connection.close()

    @staticmethod
    def add_user(name: str, surname: str, database_name="cinema_reservation_db.sqlite"):
        if path.exists(database_name):
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (name, surname) VALUES (?, ?)", (name, surname)
            )
            connection.commit()
            connection.close()
