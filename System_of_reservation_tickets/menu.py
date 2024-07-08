from repertoire import Repertoire
from datetime import datetime, timedelta

class Menu:
    def __init__(self):
        self.__option = '0'
        self.__message = ''
        self.__present_obj = None

    def __str__(self):
        message = ''
        if self.option in ['0', 'z', 'Z']:
            message += 'Witamy w naszym kinie! Wybierz jedną z opcji poniżej\n'
            message += ('1. Cennik\n'
                        '2. Repertuar\n'
                        '3. Wyświetl koszyk\n'
                        '4. Zakończ program\n')
            return message
        match self.option:
            case '1':
                message += 'Wybrano cennik'
            case '2':
                # dla 0, 1 i 2 obsługuje repertuar a dla 3 obsluguje sale
                match self.__present_obj.mode:
                    case '0' | 0:
                        message += ''
                        end_date_week = datetime.now() + timedelta(days=7)
                        message += (f'Repertuar na aktualny tydzień '
                                    f'{datetime.today().strftime("%Y-%m-%d")} - {end_date_week.strftime("%Y-%m-%d")}:\n')
                        for title in self.__present_obj.titles:
                            message += f'{self.__present_obj.titles.index(title) + 1}: {title}\n'
                        # message += 'Wybierz film lub (z)rezygnuj: '
                    case '1' | 1:
                        if isinstance(self.__present_obj, Repertoire):
                            message += f'Seans filmu "{self.__present_obj.selected_movie}" odbywa się w dniach: \n'
                            for date in self.__present_obj.dates_selected_movie:
                                message += f'{self.__present_obj.dates_selected_movie.index(date) + 1}: {date}\n'
                        else:
                            raise ValueError('Obiekt self.__present_obj dla case in [0, 1, 2] nie jest typu Repertoire')
                    case '2' | 2:
                        if isinstance(self.__present_obj, Repertoire):
                            message += (f'Dnia {self.__present_obj.selected_date} '
                                        f'film {self.__present_obj.selected_movie} '
                                        f'grany jest w następujących godzinach: \n')
                            for hour in self.__present_obj.hours_selected_movie:
                                message += f'{self.__present_obj.hours_selected_movie.index(hour) + 1}: {hour}\n'
                            # message += 'Wybierz godzinę lub (z)rezygnuj'
                        else:
                            raise ValueError("Obiekt self.__present_obj dla case in ['0', '1', '2'] "
                                             "nie jest typu Repertoire")
                    case '3' | 3:
                        message += (f'Legenda sali na film {self.__present_obj.selected_movie} grany dnia '
                                    f'{self.__present_obj.selected_date} o godznie {self.__present_obj.selected_hour}:\n'
                                    f'{self.__present_obj.cinema_hall_by_movie_date_hour}\n'
                                    f'* - wolne miejsce\n'
                                    f'X - zajęte miejsce')
            case '3':
                message += 'Wybrano wyświetl koszyk'
            case _:
                message += 'Nie wybrano żadnej z dostępnych opcji!'
        return message

    def get_object_to_present(self, value):
        if isinstance(value, Repertoire):
            self.__present_obj = value
        else:
            raise ValueError('Przekazywany obiekt nie jest Repertoire!')

    def __checking_instance_present_obj(self) -> ValueError | None:
        pass

    @property
    def option(self) -> str:
        return self.__option

    @option.setter
    def option(self, value) -> None:
        self.__option = value
