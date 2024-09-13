import random
from datetime import datetime, timedelta
import pendulum
from database_manager import DatabaseManager


class SeanceGenerator:
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
        DatabaseManager.save_to_seance_table(data)

    def prepare_data(self, last_showdate) -> None:
        # przygotowujemy daty na przyszły, aktualny tydzień
        today = datetime.today().date()
        start_date = last_showdate + timedelta(days=1)
        end_date = today + timedelta(days=self.DAYS_NUMBERS)

        next_week_show_dates = [
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((end_date - start_date).days + 1)
        ]

        movies = DatabaseManager.get_movies()
        cinema_shows = []

        for _ in range(30):
            random_movie = random.choice(movies)
            show_date = random.choice(next_week_show_dates)
            show_hour = random.choice(self.SHOW_HOURS)
            hall_number = random.choice(self.HALL_NUMBERS)
            show_datetime_string = f"{show_date} {show_hour}"
            cinema_shows.append(
                [
                    pendulum.from_format(show_datetime_string, "YYYY-MM-DD HH:mm").to_datetime_string(),
                    hall_number,
                    random_movie
                ]
            )

        # Sortowanie danych według daty seansu i godziny seansu
        cinema_shows = sorted(cinema_shows[1:], key=lambda x: (x[1], x[2]))
        SeanceGenerator.__write_to_database(cinema_shows)

    def generate_seance(self):
        today = datetime.today().date()
        last_showdate_str = DatabaseManager.get_last_showdate_from_repertoire()

        # Pobieramy z bazy ostatnią date repertuaru i sprawdzamy, czy najpóźniejszy seans jest przynajmniej 7 dni
        # do przodu od dzisiejszej daty. Jeśli nie, wygenerujemy nowe seanse do 7 dni do przodu
        if last_showdate_str and datetime.strptime(
            last_showdate_str, "%Y-%m-%d %H:%M:%S"
        ).date() >= today + timedelta(days=self.DAYS_NUMBERS):
            print("Repertuar jest aktualny")
        else:
            print("Aktualizuję repertuar.")
            last_showdate = datetime.strptime(last_showdate_str, "%Y-%m-%d %H:%M:%S").date() if last_showdate_str else today
            self.prepare_data(last_showdate)
