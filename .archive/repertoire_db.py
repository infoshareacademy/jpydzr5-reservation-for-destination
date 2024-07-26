import sqlite3
from os import path


class RepertoireDB:
    @staticmethod
    def create_table(database_name="cinema_reservation_db.sqlite"):
        if not path.exists(database_name):
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE repertoire (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_title VARCHAR(100),
                show_date VARCHAR(10),
                show_hour VARCHAR(5),
                hall_number INTEGER,
                price FLOAT)
            """
            )
            connection.commit()
            connection.close()

    @staticmethod
    def get_first_showdate_from_repertoire(
        database_name="cinema_reservation_db.sqlite",
    ) -> str or None:
        if path.exists(database_name):
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()
            cursor.execute(
                "SELECT show_date FROM repertoire ORDER BY show_date LIMIT 1"
            )
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            if results:
                first_show_date = results[0][0]
                return first_show_date
            else:
                return None
        else:
            return None

    @staticmethod
    def get_all() -> list:
        connection = sqlite3.connect("cinema_reservation_db.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM repertoire")
        list_data = list(cursor.fetchall())
        connection.close()
        return list_data

    @staticmethod
    def delete_all(database_name="cinema_reservation_db.sqlite"):
        if path.exists(database_name):
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM repertoire")
            connection.commit()
            connection.close()

    @staticmethod
    def save_to_database(data: list):
        connection = sqlite3.connect("cinema_reservation_db.sqlite")
        cursor = connection.cursor()
        for item in data:
            cursor.execute(
                "INSERT INTO repertoire (movie_title, show_date, show_hour, hall_number, price) VALUES (?,?,?,?,?)",
                item,
            )
        connection.commit()
        connection.close()
