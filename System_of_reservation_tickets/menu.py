class Menu:
    def __init__(self):
        self.__option = '0'

    def __str__(self):
        message = ''
        match self.option:
            case '0':
                message += 'Witamy w naszym kinie! Wybierz jedną z opcji poniżej\n'
                message += ('1. Cennik\n'
                            '2. Repertuar\n'
                            '3. Wyświetl koszyk\n'
                            '4. Zakończ program\n')
            case '1':
                message += 'Wybrano cennik'
            case '2':
                message += 'Wybrano repertuar'
            case '3':
                message += 'Wybrano wyświetl koszyk'
            case _:
                message += 'Nie wybrano żadnej z dostępnych opcji!'
        return message

    @property
    def option(self) -> str:
        return self.__option

    @option.setter
    def option(self, value) -> None:
        try:
            if value.isdigit() and 0 > int(value) < 4:
                print('Proszę wprowdzić wartość z przedziału <1,4>: ')
                self.__option = '0'
            else:
                self.__option = value
        except ValueError:
            print('Wprowadzono niepoprawną wartość!')
            self.__option = '0'
