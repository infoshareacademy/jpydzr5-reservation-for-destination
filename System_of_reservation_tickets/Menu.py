class Menu:
    def __init__(self):
        self.__option = None

    def __str__(self):
        return """ 
        1. Zarezerwuj bilet
        2. Wyświetl koszyk
        3. Usuń pozycję z koszyka
        4. Zakup bilet
        5. Zakończ program"""

    def choose_option(self):
        self._option = input('Wybierz opcję: ')
        match self._option:
            case '1':
                print('Wybrano "Zarezerwuj bilet"')
                return self._option
            case '2':
                print('Wybrano "Wyświetl koszyk"')
                return self._option
            case '3':
                print('Wybrano "Usuń pozycję z koszyka"')
                return self._option
            case '4':
                print('Wybrano "Zakup bilet"')
                return self._option
            case '5':
                print('Wybrano "Zakończ program"')
                return self._option

    @property
    def _option(self):
        return self.__option

    @_option.setter
    def _option(self, value):
        try:
            if int(value) < 1 or int(value) > 5:
                print('Proszę wprowdzić wartość z przedziału <1,5>: ')
                self.__option = '0'
            else:
                self.__option = value
        except ValueError:
            print('Wprowadzono niepoprawną wartość!')
            self.__option = '0'
