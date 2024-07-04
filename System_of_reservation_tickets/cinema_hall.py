class CinemaHall:
    # Na początek taki rozmiar sali, w przyszłości pewnie zmienimy
    MAX_NUMBER_OF_SEATS = 10
    MAX_NUMBER_OF_ROWS = 5

    def __init__(self, rows: int, seats: int):
        if rows > self.MAX_NUMBER_OF_ROWS or seats > self.MAX_NUMBER_OF_SEATS:
            raise ValueError(f'Maksymalna liczba rzędów wynosi {self.MAX_NUMBER_OF_ROWS}'
                             f' a miejsc siędzących {self.MAX_NUMBER_OF_SEATS}')
        self.__rows = rows
        self.__seats = []
        self.__mode = ''
        self.__date = ''  # do wykorzystania w przyszłości
        self.__hour = ''  # do wykorzystanie w przyszłości
        sign_of_row = 'A'
        # Na razie założyłem ze sala jest "kwadratowa" to znaczy każdy rząd ma tyle samo miejsc
        for i in range(rows):
            row = [sign_of_row, ['*' for _ in range(seats)]]
            self.__seats.append(row)
            sign_of_row = chr(ord(sign_of_row) + 1)

    def book_seat(self, row: str, place_seat: str):
        if row in ['z', 'Z'] or place_seat in ['z', 'Z']:
            self.mode = -1
            return
        is_all_seats_reserved = self.__check_all_seats_are_reserved_or_empty('r')
        if is_all_seats_reserved:
            print('Wszystkie miejsca w sali są zajęte!')
        else:
            self.__serve_seat(row, int(place_seat), 'r')

    def cancel_seat(self, row: str, place_seat: int) -> None:
        is_all_seats_free = self.__check_all_seats_are_reserved_or_empty('e')
        if is_all_seats_free:
            print('Wszystkie miejsca w sali są wolne!')
        else:
            self.__serve_seat(row, place_seat, 'c')

    # Wewnęczne "API" do obsługi reserwacji/odwołąnia miejsca
    def __serve_seat(self, row: str, place_seat: int, type_operation: str) -> None:
        if row in self.rows:
            for i in range(self._len_rows):
                if row == self.rows[i]:
                    if 0 < place_seat < len(self.__seats[i][1]) + 1:
                        if type_operation == 'r':
                            if self.__seats[i][1][place_seat - 1] == '*':
                                self.__seats[i][1][place_seat - 1] = 'X'
                                print(f'Miejsce {place_seat} w rzędzie {self.__seats[i][0]} zostało zarezertowane')
                            else:
                                print(f'Miejsce z rzędzie {row} o mumerze {place_seat} jest zajęte!')
                        elif type_operation == 'c':
                            if self.__seats[i][1][place_seat - 1] == 'X':
                                self.__seats[i][1][place_seat - 1] = '*'
                                print(f'Miejsce {place_seat} w rzędzie {self.__seats[i][0]} zostało anulowane')
                            else:
                                print(f'Miejsce w rzędzie {row} o mumerze {place_seat} jest wolne!')
                        else:
                            raise ValueError('Podano błędy parametr w obsłudze miejsca!')
                    else:
                        print(f'Podano numer miejsca {place_seat} w rzędzie {self.rows[i]}, którego nie ma!')
                        break
        else:
            print(f'Nie ma takiego rzedzu o symbolu {row}!')

    def __check_all_seats_are_reserved_or_empty(self, mode: str) -> bool:
        # Dla mode = 'r' sprawdzam czy wszystkie miejsca są zajęte.
        # Dla mode = 'e' sprawdzam czy wszsytkie miejsca są wolne.
        if mode not in ('r', 'e'):
            raise ValueError("Parametr 'mode' powinien być równy 'r' lub 'e'."
                             "Sprawdź wywołanie metody __check_all_seats_are_reserved_or_empty"
                             " w kodzie!")
        check_seat = 'X' if mode == 'r' else '*'
        count_all_seats_reserved_in_row = 0
        for i in range(self._len_rows):
            if all(seat == check_seat for seat in self.__seats[i][1]):
                count_all_seats_reserved_in_row += 1
        return True if count_all_seats_reserved_in_row == self._len_rows else False

    @property
    def rows(self):
        return self.__rows

    @property
    def _len_rows(self):
        return len(self.rows)

    @rows.getter
    def rows(self) -> list[str]:
        return [chr(ord('A') + i) for i in range(self.__rows)]

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        self.__mode = value

    def __str__(self) -> str:
        result = ''
        result += '\n'.join([str(i) for i in self.__seats])
        return result
