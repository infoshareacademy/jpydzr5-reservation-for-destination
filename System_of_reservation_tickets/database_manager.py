import sqlite3
from os import path


class DatabaseManager:
    @staticmethod
    def save_to_database(data: list):
        connection = sqlite3.connect("Movies.sqlite")
        cursor = connection.cursor()
        for item in data:
            cursor.execute("INSERT INTO movies VALUES (?,?,?,?,?,?,?)", item)
        connection.commit()
        connection.close()

    @staticmethod
    def delete_all_from_movies(database_name="Movies.sqlite"):
        if path.exists(database_name):
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM movies")
            connection.commit()
            connection.close()

    @staticmethod
    def get_list_table_from_database() -> list:
        connection = sqlite3.connect("Movies.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM movies")
        list_data = list(cursor.fetchall())
        connection.close()
        return list_data

    @staticmethod
    def get_first_showdate_from_database(database_name="Movies.sqlite") -> str or None:
        if path.exists(database_name):
            connection = sqlite3.connect("Movies.sqlite")
            cursor = connection.cursor()
            cursor.execute("SELECT Show_date FROM Movies ORDER BY Show_date LIMIT 1")
            first_show_date = cursor.fetchall()[0][0]
            cursor.close()
            connection.close()
            return first_show_date
        else:
            return None

    @staticmethod
    def create_date_base(database_name="Movies.sqlite"):
        if not path.exists(database_name):
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()
            cursor.execute(
                "CREATE TABLE Movies ("
                "Movie_title varchar(100),"
                "Show_date varchar(10),"
                "Show_hour varchar(5),"
                "Hall_number integer,"
                "Price float,"
                "Row varchar(1),"
                "Seat integer)"
            )
            connection.commit()
            connection.close()
