import csv

# Zaczytanie danych do zmiennej 'file'

file = []

try:
    with open('data_base.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        file.append(row)
except FileNotFoundError:
    print("Plik 'data_base.csv' nie został znaleziony.")
except csv.Error as e:
    print(f"Błąd odczytu pliku CSV: {e}")

# Wyświetlanie zmiennej 'file'

for row in file:
    print(row)



