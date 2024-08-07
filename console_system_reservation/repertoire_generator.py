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
        DatabaseManager.create_databases()
        DatabaseManager.save_to_repertoire(data)

    def prepare_data(self, last_showdate) -> None:
        # przygotowujemy daty na przyszły, aktualny tydzień
        today = datetime.today().date()
        start_date = last_showdate + timedelta(days=1)
        end_date = today + timedelta(days=self.DAYS_NUMBERS)

        next_week_show_dates = [
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((end_date - start_date).days + 1)
        ]

        # Generowanie 30 przykładowych danych seansów
        cinema_shows = [
            ["Movie_title", "Show_date", "Show_hour", "Hall_number", "Price"]
        ]
        price_list = PriceList()
        normal_price = price_list.get_price_by_name("Normalny")
        for _ in range(30):
            movie_title = random.choice(self.MOVIE_TITLES)
            show_date = random.choice(next_week_show_dates)
            show_hour = random.choice(self.SHOW_HOURS)
            hall_number = random.choice(self.HALL_NUMBERS)
            price = normal_price
            cinema_shows.append([movie_title, show_date, show_hour, hall_number, price])

        # Sortowanie danych według daty seansu i godziny seansu
        cinema_shows = sorted(cinema_shows[1:], key=lambda x: (x[1], x[2]))
        RepertoireGenerator.__write_to_database(cinema_shows)

    def check_repertoire_date(self):
        today = datetime.today().date()
        last_showdate_str = DatabaseManager.get_last_showdate_from_repertoire()
        last_showdate = datetime.strptime(last_showdate_str, "%Y-%m-%d").date()

        # Pobieramy z bazy ostatnią date repertuaru i sprawdzamy, czy najpóźniejszy seans jest przynajmniej 7 dni
        # do przodu od dzisiejszej daty. Jeśli nie, wygenerujemy nowe seanse do 7 dni do przodu
        if (
            last_showdate >= today + timedelta(days=self.DAYS_NUMBERS)
        ):
            print("Repertuar jest aktualny")
        else:
            print("Aktualizuję repertuar.")
            self.prepare_data(last_showdate)
