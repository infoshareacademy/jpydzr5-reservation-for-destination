class Ticket:
    def __init__(self, movie_title: str, show_date: str, show_hour: str, hall_number: int, price: float, row: str,
                 seat: int):
        self.__movie_title = movie_title
        self.__show_date = show_date
        self.__show_hour = show_hour
        self.__hall_number = hall_number
        self.__price = price
        self.__row = row
        self.__seat = seat

    def __str__(self):
        return (f'Tytuł filmu: {self.__movie_title}, '
                f'Data seansu: {self.__show_date}, '
                f'Godzina seansu: {self.__show_hour}, '
                f'Numer sali: {self.__hall_number}, '
                f'Rząd: {self.__row}, '
                f'Miejsce: {self.__seat}, '
                f'Cena: {self.__price:.2f} PLN\n')

    # Zmiana rzędu i miejsca oraz wyświetlenie komunikatu o zmianie
    # TODO: W przyszłości będziemy sprawdzać czy takie rzędy/miejsca istnieją i są wolne
    def change_seat(self, new_row: str, new_seat: int):
        self.__row = new_row
        self.__seat = new_seat
        print(f"Miejsce zmienione na rząd: {self.__row}, miejsce: {self.__seat}.")

    # Zastosowanie zniżki do ceny biletu i wyświetlenie nowej ceny
    def apply_discount(self, discount_percent: int):
        if 0 < discount_percent < 100:
            discount = (self.__price * discount_percent) / 100
            self.__price -= discount
            print(f"Zastosowano zniżkę: {discount_percent}%, nowa cena: {self.__price:.2f} PLN")
        else:
            print("Nieprawidłowy rabat. Proszę wpisać wartość w zakresie 0-100.")

    @property
    def price(self) -> float:
        return self.__price