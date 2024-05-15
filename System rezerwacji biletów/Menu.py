class Menu:
    def __init__(self):
        self._option = None

    def __str__(self):
        return """ 
        1. Zarezerwuj bilet
        2. Wyświetl koszyk
        3. Usuń pozycję z koszyka
        4. Zakup bilet
        5. Zakończ program"""

    def choose_option(self):
        option = input('Wybierz opcję: ')
        self._option = option
        match option:
            case '1':
                print('Wybrano "Zarezerwuj bilet"')
                return option
            case '2':
                print('Wybrano "Wyświetl koszyk"')
                return option
            case '3':
                print('Wybrano "Usuń pozycję z koszyka"')
                return option
            case '4':
                print('Wybrano "Zakup bilet"')
                return option
            case '5':
                print('Wybrano "Zakończ program"')
                return option
            case _:
                print('Nie wybrano żadnej z dostępnej opcji')
