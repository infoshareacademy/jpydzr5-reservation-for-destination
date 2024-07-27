import sqlite3
from os import path


class ReservationsDB:
    @staticmethod
    def create_table(database_name="cinema_reservation_db.sqlite"):
        if not path.exists(database_name):
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()
            cursor.execute(
                "CREATE TABLE reservations ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "repertoire_id INTEGER NOT NULL,"
                "user_id INTEGER NOT NULL,"
                "row VARCHAR(1) NOT NULL,"
                "seat INTEGER NOT NULL,"
                "FOREIGN KEY (repertoire_id) REFERENCES repertoire(id)"
                "FOREIGN KEY (user_id) REFERENCES users(id))"
            )
            connection.commit()
            connection.close()

    @staticmethod
    def add_reservation(
        repertoire_id: int,
        user_id: int,
        row: str,
        seat: int,
        database_name="cinema_reservation_db" ".sqlite",
    ):
        if path.exists(database_name):
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM reservations"
                "WHERE repertoire_id = ? AND row = ? AND seat = ?",
                (repertoire_id, row, seat),
            )
            result = cursor.fetchone()
            if result:
                print("Miejsce jest już zarezerwowane.")
            else:
                cursor.execute(
                    "INSERT INTO reservations (repertoire_id, user_id, row, seat)"
                    "VALUES (?, ?, ?, ?)",
                    (repertoire_id, user_id, row, seat),
                )
            connection.commit()
            connection.close()
