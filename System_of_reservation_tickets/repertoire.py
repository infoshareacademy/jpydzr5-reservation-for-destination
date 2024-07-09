from copy import deepcopy
from csv import reader
from cinema_hall import CinemaHall
from csvGenerator import CSVGenerator


class Repertoire:
    def __init__(self, cinema_hall: CinemaHall):
        self.__mode = '0'
        self.__selected_movie = ''
        self.__selected_date = ''
        self.__selected_hour = ''
        self.__movies_dict = dict()

        generator = CSVGenerator()
        generator.check_database_date()
        csvfile = generator.read_csv_database()
        for row in csvfile:
            movie_title = row[0]
            show_date = row[1]
            hour_of_movie = row[2]

            if movie_title not in self.__movies_dict:
                self.__movies_dict[movie_title] = {}

            if show_date not in self.__movies_dict[movie_title]:
                self.__movies_dict[movie_title][show_date] = {}

            if hour_of_movie not in self.__movies_dict[movie_title][show_date]:
                self.__movies_dict[movie_title][show_date][hour_of_movie] = {}

            self.__movies_dict[movie_title][show_date][hour_of_movie] = deepcopy(cinema_hall)

    def choose_row(self, row: str) -> str | ValueError | None:
        if row in ['z', 'Z']:
            self.mode = -1
            return
        elif row.upper() in self.cinema_hall_by_movie_date_hour.rows:
            return row
        else:
            raise ValueError('Wskazano nieprawidłowy rząd!')

    def choose_seat(self, seat: str) -> str | None:
        if seat in ['z', 'Z']:
            self.mode = -1
            return
        return seat

    def get_cinema_hall_by_movie_date_hour(self, title: str, date: str, hour: str) -> CinemaHall:
        self.mode = 0
        return self.__movies_dict[title][date][hour]

    @property
    def dates_selected_movie(self):
        if self.selected_movie:
            return [date for date in self.__movies_dict[self.selected_movie].keys()]
        else:
            raise ValueError('Nie wybrano filmu! Pierw należy wybrać tytuł filmu!')

    @property
    def hours_selected_movie(self):
        if self.__selected_date:
            return [hour for hour in self.__movies_dict[self.selected_movie][self.__selected_date].keys()]

    @property
    def titles(self):
        return [title for title in self.__movies_dict.keys()]

    @property
    def selected_movie(self):
        return self.__selected_movie

    @property
    def selected_date(self):
        return self.__selected_date

    @property
    def __len_hours(self) -> len:
        return len([self.__movies_dict[self.selected_movie][self.__selected_date]])

    @property
    def cinema_hall_by_movie_date_hour(self):
        return self.__movies_dict[self.selected_movie][self.selected_date][self.__selected_hour]

    @property
    def selected_hour(self):
        return self.__selected_hour

    @property
    def __len_dates(self) -> len:
        return len(self.dates_selected_movie)

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        self.__mode = value

    def get_movie_by_index(self, index: str) -> str | None:
        if index in ['Z', 'z']:
            self.__mode = -1
            return
        index = int(index)
        if 0 < index <= len(self.titles):
            self.mode = 1
            self.__selected_movie = self.titles[index - 1]
            return self.titles[index - 1]
        else:
            raise ValueError('Index wykracza poza zakres danych!')

    def get_date_by_index(self, index: str) -> str | None:
        if index in ['Z', 'z']:
            self.__mode = -1
            return index
        index = int(index)
        if 0 < index <= self.__len_dates:
            self.mode = 2
            self.__selected_date = self.dates_selected_movie[index - 1]
            return self.dates_selected_movie[index - 1]
        else:
            raise ValueError('Index wykracza poza zakres danych!')

    def get_hour_by_index(self, index: str) -> str | None:
        if index in ['Z', 'z']:
            self.__mode = -1
            return index
        index = int(index)
        if 0 < index <= self.__len_hours:
            self.mode = 3
            self.__selected_hour = self.hours_selected_movie[index - 1]
            return self.hours_selected_movie[index - 1]
        else:
            raise ValueError('Index wykracza poza zakres danych!')
