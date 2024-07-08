import csv
import random
from datetime import datetime, timedelta


class CSVGenerator:
    # Na początek zestaw domyślnych danych, w przyszłości możemy je zmieniać
    MOVIE_TITLES = ["Avengers: Endgame", "The Godfather", "Inception", "The Shawshank Redemption", "The Dark Knight",
                    "Pulp Fiction", "Forrest Gump", "The Matrix", "Schindler's List", "Titanic"]
    SHOW_HOURS = ["10:00", "13:30", "16:45", "19:30", "22:15"]
    HALL_NUMBERS = ["1"]
    PRICES = [15.00, 18.00, 20.00, 22.00, 25.00]
    ROWS = ["A", "B", "C", "D", "E"]
    SEATS = [str(i) for i in range(1, 11)]
    FILE_PATH = "data_base.csv"
    DAYS_NUMBERS = 7

    def __generate_show_dates(self):
        today = datetime.today()
        show_dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(self.DAYS_NUMBERS)]
        return show_dates

    def __write_to_file(self, cinema_shows):
        try:
            with open(self.FILE_PATH, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for cinema_row in cinema_shows:
                    writer.writerow(cinema_row)
            print("Plik CSV został utworzony pomyślnie!")
        except IOError as e:
            print(f"Podczas tworzenia pliku CSV wystąpił błąd: {e}")

    def __generate_csv_database(self):
        generated_show_dates = self.__generate_show_dates()

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

        # Zapis do pliku CSV
        self.__write_to_file(cinema_shows)

    def check_database_date(self):
        first_date = self.__get_first_date()
        today = datetime.today()
        if first_date and datetime.strptime(first_date, "%Y-%m-%d").date() >= today.date():
            print("Repertuar jest aktualny")
        else:
            print("Aktualizuję repertuar.")
            self.__generate_csv_database()

    def __get_first_date(self):
        data = self.read_csv_database()
        if data and len(data) > 0:
            # Odczytujemy pierwszą wartość z kolumny show_dates, jest to druga kolumna, indeks 1
            first_date = data[0][1]
            return first_date
        else:
            return None

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


