class Ticket:
    def __init__(self, tytul_filmu, data_seansu, godzina_seansu, numer_sali, cena_biletu, rzad, miejsce):
        self.tytul_filmu = tytul_filmu
        self.data_seansu = data_seansu
        self.godzina_seansu = godzina_seansu
        self.numer_sali = numer_sali
        self.cena_biletu = cena_biletu
        self.rzad = rzad
        self.miejsce = miejsce

    def __str__(self):
        return (f"Szczegóły Biletu:\n"
                f"Tytuł Filmu: {self.tytul_filmu}\n"
                f"Data Seansu: {self.data_seansu}\n"
                f"Godzina Seansu: {self.godzina_seansu}\n"
                f"Numer Sali: {self.numer_sali}\n"
                f"Cena Biletu: {self.cena_biletu:.2f} zł\n"
                f"Rząd: {self.rzad}\n"
                f"Miejsce: {self.miejsce}\n")

    def change_seat(self, nowy_rzad, nowe_miejsce):
        # Zmiana rzędu i miejsca oraz wyświetlenie komunikatu o zmianie
        self.rzad = nowy_rzad
        self.miejsce = nowe_miejsce
        print(f"Miejsce zmienione na Rząd: {self.rzad}, Miejsce: {self.miejsce}")

    def apply_discount(self, procent_rabatu):
        # Zastosowanie rabatu do ceny biletu i wyświetlenie nowej ceny
        if 0 < procent_rabatu < 100:
            kwota_rabatu = (self.cena_biletu * procent_rabatu) / 100
            self.cena_biletu -= kwota_rabatu
            print(f"Rabat zastosowany: {procent_rabatu}%, Nowa Cena: {self.cena_biletu:.2f} zł")
        else:
            print("Nieprawidłowy procent rabatu. Powinien być między 0 a 100.")
