import sqlite3
from os import path


class DatabaseManager:
    DATABASE_PATH = "../cinema_reservation_system/db.sqlite3"
    SEANCE_TABLE_NAME = "cinema_seance"
    MOVIE_TABLE_NAME = "cinema_movie"

    @staticmethod
    def create_connection(database_path: str) -> sqlite3.Connection:
        if path.exists(DatabaseManager.DATABASE_PATH):
            connection = sqlite3.connect(database_path)
            return connection
        else:
            raise Exception("Baza danych nie istnieje.")

    @staticmethod
    def get_last_showdate_from_repertoire() -> str or None:
        connection = DatabaseManager.create_connection(DatabaseManager.DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute(f"SELECT show_start FROM {DatabaseManager.SEANCE_TABLE_NAME} ORDER BY show_start DESC LIMIT 1")
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        if results:
            return results[0][0]
        else:
            return None

    @staticmethod
    def get_movies():
        connection = DatabaseManager.create_connection(DatabaseManager.DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute(f"SELECT id FROM {DatabaseManager.MOVIE_TABLE_NAME}")
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        if results:
            return [item[0] for item in results]
        else:
            raise Exception("Brak filmów. Zasil tabelę z pliku movies.json")

    @staticmethod
    def save_to_seance_table(data: list):
        connection = DatabaseManager.create_connection(DatabaseManager.DATABASE_PATH)
        cursor = connection.cursor()
        for element in data:
            cursor.execute(
                "INSERT INTO cinema_seance (show_start, hall_number, movie_id) VALUES (?, ?, ?)",
                element
            )
        connection.commit()
        connection.close()
