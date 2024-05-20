import csv
import random

# Przykładowe dane filmów, dni i godzin seansów
tytuly_filmow = ["Avengers: Endgame", "The Godfather", "Inception", "The Shawshank Redemption", "The Dark Knight",
                 "Pulp Fiction", "Forrest Gump", "The Matrix", "Schindler's List", "Titanic"]
dni_seansow = ["2024-05-15", "2024-05-16", "2024-05-17", "2024-05-18", "2024-05-19"]
godziny_seansow = ["10:00", "13:30", "16:45", "19:30", "22:15"]
numery_sali = ["1", "2", "3", "4", "5"]
ceny_biletow = ["15.00", "18.00", "20.00", "22.00", "25.00"]
rzedy = ["A", "B", "C", "D", "E"]
miejsca = [str(i) for i in range(1, 11)]

# Generowanie 30 przykładowych danych seansów
dane_seansow = [["Tytuł filmu", "Data seansu", "Godzina seansu", "Numer Sali", "Cena biletu", "Rząd", "Miejsce"]]
for _ in range(30):
    tytul_filmu = random.choice(tytuly_filmow)
    data_seansu = random.choice(dni_seansow)
    godzina_seansu = random.choice(godziny_seansow)
    numer_sali = random.choice(numery_sali)
    cena_biletu = random.choice(ceny_biletow)
    rząd = random.choice(rzedy)
    miejsce = random.choice(miejsca)
    dane_seansow.append([tytul_filmu, data_seansu, godzina_seansu, numer_sali, cena_biletu, rząd, miejsce])

# Ścieżka do pliku CSV
sciezka_pliku = "data_base.csv"

# Zapis do pliku CSV
try:
    with open(sciezka_pliku, mode='w', newline='') as plik_csv:
        writer = csv.writer(plik_csv)
        for wiersz in dane_seansow:
            writer.writerow(wiersz)
    print("Plik CSV został utworzony pomyślnie!")
except IOError as e:
    print(f"Podczas tworzenia pliku CSV wystąpił błąd: {e}")
