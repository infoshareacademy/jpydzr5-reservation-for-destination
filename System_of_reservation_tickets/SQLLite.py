import sqlite3
from os import path


class SQLLite:
    @staticmethod
    def __import_from_csv_to_database():
        connection = sqlite3.connect('Movies.sqlite')
        cursor = connection.cursor()
        with open('data_base.csv', mode='r') as csv_file:
            for row in csv_file:
                cursor.execute("INSERT INTO movies VALUES (?,?,?,?,?,?,?)", row.split(','))
                connection.commit()
            connection.close()

    @staticmethod
    def delete_all_from_movies(database_name='Movies.sqlite'):
        if path.exists(database_name):
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM movies")

    @staticmethod
    def get_list_table_from_database() -> list:
        SQLLite.__import_from_csv_to_database()
        connection = sqlite3.connect('Movies.sqlite')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM movies")
        list_data = list(cursor.fetchall())
        connection.close()
        return list_data

    @staticmethod
    def create_date_base(database_name='Movies.sqlite'):
        if not path.exists(database_name):
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE Movies ("
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