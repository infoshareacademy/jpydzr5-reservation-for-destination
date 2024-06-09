import csv
import random

# Przykładowe dane filmów, dni i godzin seansów
film_titles = ["Avengers: Endgame", "The Godfather", "Inception", "The Shawshank Redemption", "The Dark Knight",
                 "Pulp Fiction", "Forrest Gump", "The Matrix", "Schindler's List", "Titanic"]
show_dates = ["2024-05-15", "2024-05-16", "2024-05-17", "2024-05-18", "2024-05-19"]
show_hours = ["10:00", "13:30", "16:45", "19:30", "22:15"]
hall_numbers = ["1", "2", "3", "4", "5"]
ticket_prices = ["15.00", "18.00", "20.00", "22.00", "25.00"]
rows = ["A", "B", "C", "D", "E"]
seats = [str(i) for i in range(1, 11)]

# Generowanie 30 przykładowych danych seansów
cinema_shows = [["Film_title", "Show_date", "Show_hour", "Hall_number", "Ticket_price", "Row", "Seat"]]
for _ in range(30):
    film_title = random.choice(film_titles)
    show_date = random.choice(show_dates)
    show_hour = random.choice(show_hours)
    hall_number = random.choice(hall_numbers)
    ticket_price = random.choice(ticket_prices)
    row = random.choice(rows)
    seat = random.choice(seats)
    cinema_shows.append([film_title, show_date, show_hour, hall_number, ticket_price, row, seat])

# Ścieżka do pliku CSV
file_path = "System rezerwacji biletów/data_base.csv"

# Zapis do pliku CSV
try:
    with open(file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for cinema_row in cinema_shows:
            writer.writerow(cinema_row)
    print("Plik CSV został utworzony pomyślnie!");
except IOError as e:
    print(f"Podczas tworzenia pliku CSV wystąpił błąd: {e}")
