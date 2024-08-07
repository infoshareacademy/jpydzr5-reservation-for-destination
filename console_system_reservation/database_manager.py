import sqlite3
from os import path

from repertoire_table import RepertoireTable
from reservations_table import ReservationsTable
from users_table import UsersTable


class DatabaseManager:
    DATABASE_NAME = "cinema_db.sqlite"

    @staticmethod
    def add_repertoire(data: list):
        RepertoireTable.add_repertoire(data)

    @staticmethod
    def delete_all_from_repertoire():
        RepertoireTable.delete_all()

    @staticmethod
    def get_list_table_from_repertoire() -> list:
        return RepertoireTable.get_all()

    @staticmethod
    def get_last_showdate_from_repertoire() -> str or None:
        return RepertoireTable.get_last_showdate_from_repertoire()

    @staticmethod
    def add_user(name: str, surname: str):
        UsersTable.add_user(name, surname)

    @staticmethod
    def add_reservation(repertoire_id: int, user_id: int, row: str, seat: int):
        ReservationsTable.add_reservation(repertoire_id, user_id, row, seat)

    @staticmethod
    def create_databases():
        if not path.exists(DatabaseManager.DATABASE_NAME):
            connection = sqlite3.connect(DatabaseManager.DATABASE_NAME)
            cursor = connection.cursor()
            RepertoireTable.create_table(cursor)
            UsersTable.create_table(cursor)
            ReservationsTable.create_table(cursor)
            connection.commit()
            connection.close()
