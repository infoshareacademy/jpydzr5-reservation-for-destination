import random
from datetime import datetime, timedelta

from database_manager import DatabaseManager
from price_list import PriceList


class RepertoireGenerator:
    MOVIE_TITLES = [
        "Avengers: Endgame",
        "The Godfather",
        "Inception",
        "The Shawshank Redemption",
        "The Dark Knight",
        "Pulp Fiction",
        "Forrest Gump",
        "The Matrix",
        "Schindler's List",
        "Titanic",
    ]
    SHOW_HOURS = ["10:00", "13:30", "16:45", "19:30", "22:15"]
    HALL_NUMBERS = ["1"]
    ROWS = ["A", "B", "C", "D", "E"]
    SEATS = [str(i) for i in range(1, 11)]
    DAYS_NUMBERS = 7

    def __generate_show_dates(self):
        today = datetime.today()
        show_dates = [
            (today + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(self.DAYS_NUMBERS)
        ]
        return show_dates

    @staticmethod
    def __write_to_database(data: list):
        DatabaseManager.create_date_base()
        DatabaseManager.delete_all_from_movies()
        DatabaseManager.save_to_database(data)

    def prepare_data(self) -> list:
        generated_show_dates = self.__generate_show_dates()

        # Generowanie 30 przykładowych danych seansów
        cinema_shows = [
            [
                "Movie_title",
                "Show_date",
                "Show_hour",
                "Hall_number",
                "Price",
                "Row",
                "Seat",
            ]
        ]
        price_list = PriceList()
        normal_price = price_list.get_price_by_name("Normalny")
        for _ in range(30):
            movie_title = random.choice(self.MOVIE_TITLES)
            show_date = random.choice(generated_show_dates)
            show_hour = random.choice(self.SHOW_HOURS)
            hall_number = random.choice(self.HALL_NUMBERS)
            price = normal_price
            row = random.choice(self.ROWS)
            seat = random.choice(self.SEATS)
            cinema_shows.append(
                [movie_title, show_date, show_hour, hall_number, price, row, seat]
            )

        # Sortowanie danych według daty seansu i godziny seansu
        cinema_shows = sorted(cinema_shows[1:], key=lambda x: (x[1], x[2]))
        RepertoireGenerator.__write_to_database(cinema_shows)

    def check_repertoire_date(self):
        today = datetime.today()
        first_showdate = DatabaseManager.get_first_showdate_from_database()
        if (
            first_showdate
            and datetime.strptime(first_showdate, "%Y-%m-%d").date() >= today.date()
        ):
            print("Repertuar jest aktualny")
        else:
            print("Aktualizuję repertuar.")
            self.prepare_data()
