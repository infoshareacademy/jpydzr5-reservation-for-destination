import csv
import random
from datetime import datetime, timedelta


class CSVGenerator:
    # Na początek zestaw domyślnych danych, w przyszłości możemy je zmieniać
    MOVIE_TITLES = ["Avengers: Endgame", "The Godfather", "Inception", "The Shawshank Redemption", "The Dark Knight",
                    "Pulp Fiction", "Forrest Gump", "The Matrix", "Schindler's List", "Titanic"]
    SHOW_HOURS = ["10:00", "13:30", "16:45", "19:30", "22:15"]
    HALL_NUMBERS = ["1", "2", "3", "4", "5"]
    PRICES = [15.00, 18.00, 20.00, 22.00, 25.00]
    ROWS = ["A", "B", "C", "D", "E"]
    SEATS = [str(i) for i in range(1, 11)]
    FILE_PATH = "data_base.csv"
    DAYS_NUMBERS = 7

    def generate_show_dates(self):
        today = datetime.today()
        show_dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(self.DAYS_NUMBERS)]
        return show_dates

    def generate_csv_database(self):
        generated_show_dates = self.generate_show_dates()

        # Generowanie 30 przykładowych danych seansów
        cinema_shows = [["Movie_title", "Show_date", "Show_hour", "Hall_number", "Price", "Row", "Seat"]]
        for _ in range(30):
            movie_title = random.choice(self.MOVIE_TITLES)
            show_date = random.choice(generated_show_dates)
            show_hour = random.choice(self.SHOW_HOURS)
            hall_number = random.choice(self.HALL_NUMBERS)
            price = random.choice(self.PRICES)
            row = random.choice(self.ROWS)
            seat = random.choice(self.SEATS)
            cinema_shows.append([movie_title, show_date, show_hour, hall_number, price, row, seat])

        # Sortowanie danych według daty seansu i godziny seansu
        cinema_shows = [cinema_shows[0]] + sorted(cinema_shows[1:], key=lambda x: (x[1], x[2]))

        # Ścieżka do pliku CSV
        file_path = self.FILE_PATH

        # Zapis do pliku CSV
        try:
            with open(file_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for cinema_row in cinema_shows:
                    writer.writerow(cinema_row)
            print("Plik CSV został utworzony pomyślnie!")
        except IOError as e:
            print(f"Podczas tworzenia pliku CSV wystąpił błąd: {e}")

    def check_database_date(self):
        try:
            with open(self.FILE_PATH, mode='r') as csv_file:
                reader = csv.reader(csv_file)
                next(reader)
                last_date = None

                for row in reader:
                    show_date = row[1]
                    if last_date is None or show_date > last_date:
                        last_date = show_date

                if last_date is None:
                    print("Repertuar jest pusty, generuję nowy.")
                    self.generate_csv_database()

                last_date = datetime.strptime(last_date, "%Y-%m-%d")
                today = datetime.today()

                if last_date.date() < today.date():
                    print("Ostatnia data seansu jest starsza niż aktualny dzień. Generuję nowy repertuar.")
                    self.generate_csv_database()
                else:
                    print("Ostatnia data seansu nie jest starsza niż aktualny dzień.")
        except FileNotFoundError:
            print("Plik CSV nie został znaleziony. Generuję nowy.")
            self.generate_csv_database()
        except IOError as e:
            print(f"Wystąpił błąd podczas odczytywania pliku CSV: {e}")

    def read_csv_database(self):
        try:
            with open(self.FILE_PATH, mode='r') as csv_file:
                reader = csv.reader(csv_file)
                # Pomijamy nagłówek
                next(reader)
                data = []
                for row in reader:
                    data.append(row)
                return data
        except FileNotFoundError:
            print("Plik CSV nie został znaleziony.")
            return None
        except IOError as e:
            print(f"Wystąpił błąd podczas odczytywania pliku CSV: {e}")
            return None
