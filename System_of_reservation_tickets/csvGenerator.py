import csv
import random
from datetime import datetime, timedelta

# Przykładowe dane filmów, dni i godzin seansów
movie_titles = ["Avengers: Endgame", "The Godfather", "Inception", "The Shawshank Redemption", "The Dark Knight",
               "Pulp Fiction", "Forrest Gump", "The Matrix", "Schindler's List", "Titanic"]
show_hours = ["10:00", "13:30", "16:45", "19:30", "22:15"]
hall_numbers = ["1", "2", "3", "4", "5"]
prices = [15.00, 18.00, 20.00, 22.00, 25.00]
rows = ["A", "B", "C", "D", "E"]
seats = [str(i) for i in range(1, 11)]


# Generowanie dat seansów w przedziale jednego tygodnia od dziś
def generate_show_dates(days_number=7):
    today = datetime.today()
    show_dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days_number)]
    return show_dates


generated_show_dates = generate_show_dates()

# Generowanie 30 przykładowych danych seansów
cinema_shows = [["Movie_title", "Show_date", "Show_hour", "Hall_number", "Price", "Row", "Seat"]]
for _ in range(30):
    movie_title = random.choice(movie_titles)
    show_date = random.choice(generated_show_dates)
    show_hour = random.choice(show_hours)
    hall_number = random.choice(hall_numbers)
    price = random.choice(prices)
    row = random.choice(rows)
    seat = random.choice(seats)
    cinema_shows.append([movie_title, show_date, show_hour, hall_number, price, row, seat])


#Sortowanie danych według daty seansu i godziny seansu
cinema_shows = [cinema_shows[0]] + sorted(cinema_shows[1:], key=lambda x: (x[1], x[2]))


# Ścieżka do pliku CSV
file_path = "data_base.csv"

# Zapis do pliku CSV
try:
    with open(file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for cinema_row in cinema_shows:
            writer.writerow(cinema_row)
    print("Plik CSV został utworzony pomyślnie!");
except IOError as e:
    print(f"Podczas tworzenia pliku CSV wystąpił błąd: {e}")
