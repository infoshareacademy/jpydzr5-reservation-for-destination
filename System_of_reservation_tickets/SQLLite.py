import sqlite3


class SQLLite:
    @staticmethod
    def __import_from_csv_to_database():
        connection = sqlite3.connect('identifier.sqlite')
        cursor = connection.cursor()
        with open('data_base.csv', mode='r') as csv_file:
            cursor.execute("DELETE FROM movies")
            for row in csv_file:
                cursor.execute("INSERT INTO movies VALUES (?,?,?,?,?,?,?)", row.split(','))
                connection.commit()
            connection.close()

    @staticmethod
    def get_list_table_from_database() -> list:
        SQLLite.__import_from_csv_to_database()
        connection = sqlite3.connect('identifier.sqlite')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM movies")
        list_data = list(cursor.fetchall())
        connection.close()
        return list_data
