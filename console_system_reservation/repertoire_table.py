import sqlite3
from os import path


class RepertoireTable:
    DATABASE_NAME = "cinema_db.sqlite"

    @staticmethod
    def create_table(cursor: sqlite3.Cursor):
        cursor.execute(
            "CREATE TABLE cinema_repertoire ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "movie_title VARCHAR(100),"
            "show_date VARCHAR(10),"
            "show_hour VARCHAR(5),"
            "hall_number INTEGER,"
            "movie_description VARCHAR(300),"
            "price FLOAT)"
        )

    @staticmethod
    def get_last_showdate_from_repertoire() -> str or None:
        if path.exists(RepertoireTable.DATABASE_NAME):
            connection = sqlite3.connect(RepertoireTable.DATABASE_NAME)
            cursor = connection.cursor()
            cursor.execute(
                "SELECT show_date FROM cinema_repertoire ORDER BY show_date DESC LIMIT 1"
            )
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            if results:
                return results[0][0]
            else:
                return None
        else:
            return None

    @staticmethod
    def get_all() -> list:
        connection = sqlite3.connect(RepertoireTable.DATABASE_NAME)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cinema_repertoire")
        list_data = list(cursor.fetchall())
        connection.close()
        return list_data

    @staticmethod
    def delete_all():
        if path.exists(RepertoireTable.DATABASE_NAME):
            connection = sqlite3.connect(RepertoireTable.DATABASE_NAME)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM cinema_repertoire")
            connection.commit()
            connection.close()

    @staticmethod
    def add_repertoire(data: list):
        connection = sqlite3.connect(RepertoireTable.DATABASE_NAME)
        cursor = connection.cursor()
        for item in data:
            cursor.execute(
                "INSERT INTO cinema_repertoire (movie_title, show_date, show_hour, hall_number,movie_description, price) VALUES (?,?,?,?,?,?)",
                item,
            )
        connection.commit()
        connection.close()
