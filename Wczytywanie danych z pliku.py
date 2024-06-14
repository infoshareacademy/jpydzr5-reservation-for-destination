import csv
import random

# Zaczytanie danych do zmiennej 'file'

with open('data_base.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    file = [row for row in reader]

# Wyświetlanie zmiennej 'file'

for row in file:
    print(row)



