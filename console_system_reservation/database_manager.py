from repertoire_db import RepertoireDB
from reservations_db import ReservationsDB
from users_db import UsersDB


class DatabaseManager:
    @staticmethod
    def save_to_repertoire(data: list):
        RepertoireDB.save_to_database(data)

    @staticmethod
    def delete_all_from_repertoire():
        RepertoireDB.delete_all()

    @staticmethod
    def get_list_table_from_repertoire() -> list:
        return RepertoireDB.get_all()

    @staticmethod
    def get_last_showdate_from_repertoire() -> str or None:
        return RepertoireDB.get_last_showdate_from_repertoire()

    @staticmethod
    def add_user(name: str, surname: str):
        UsersDB.add_user(name, surname)

    @staticmethod
    def add_reservation(repertoire_id: int, user_id: int, row: str, seat: int):
        ReservationsDB.add_reservation(repertoire_id, user_id, row, seat)

    @staticmethod
    def create_databases():
        RepertoireDB.create_table()
        UsersDB.create_table()
        ReservationsDB.create_table()
