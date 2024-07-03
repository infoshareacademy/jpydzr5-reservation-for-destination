class Ticket:
    def __init__(self, movie_title: str, show_date: str, show_hour: str, hall_number: int, price: float, row: str,
                 seat: int):
        self.movie_title = movie_title
        self.show_date = show_date
        self.show_hour = show_hour
        self.hall_number = hall_number
        self.price = price
        self.row = row
        self.seat = seat

    def __str__(self):
        return (f"Szczegóły biletu: \n"
                f"Tytuł filmu: {self.movie_title}\n"
                f"Data seansu: {self.show_date}\n"
                f"Godzina seansu: {self.show_hour}\n"
                f"Numer sali: {self.hall_number}\n"
                f"Rząd: {self.row}\n"
                f"Miejsce: {self.seat}\n"
                f"Cena: {self.price:.2f} PLN\n")

    # Zmiana rzędu i miejsca oraz wyświetlenie komunikatu o zmianie
    # TODO: W przyszłości będziemy sprawdzać czy takie rzędy/miejsca istnieją i są wolne
    def change_seat(self, new_row: str, new_seat: int):
        self.row = new_row
        self.seat = new_seat
        print(f"Miejsce zmienione na rząd: {self.row}, miejsce: {self.seat}.")

    # Zastosowanie zniżki do ceny biletu i wyświetlenie nowej ceny
    def apply_discount(self, discount_percent: int):
        if 0 < discount_percent < 100:
            discount = (self.price * discount_percent) / 100
            self.price -= discount
            print(f"Zastosowano zniżkę: {discount_percent}%, nowa cena: {self.price:.2f} PLN")
        else:
            print("Nieprawidłowy rabat. Proszę wpisać wartość w zakresie 0-100.")
