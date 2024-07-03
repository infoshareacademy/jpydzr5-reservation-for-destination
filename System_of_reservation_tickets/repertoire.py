import csv
from datetime import datetime

from dateutil.parser import parse


class Repertoire:
    def __init__(self):
        self.__mode = '0'
        self.__selected_movie = ''
        self.__selected_date = ''
        self.__selected_hour = ''
        self.movies_dict = dict()
        with open('data_base.csv', 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)
            for row in csv_reader:
                movie_title = row[0]
                show_date = row[1]
                hour_of_movie = row[2]
                row_of_seat = row[3]
                place_of_seat = row[4]

                if movie_title not in self.movies_dict:
                    self.movies_dict[movie_title] = {}

                if show_date not in self.movies_dict[movie_title]:
                    self.movies_dict[movie_title][show_date] = {}

                if hour_of_movie not in self.movies_dict[movie_title][show_date]:
                    self.movies_dict[movie_title][show_date][hour_of_movie] = {}

                self.movies_dict[movie_title][show_date][hour_of_movie][row_of_seat] = [place_of_seat]

    @property
    def dates_selected_movie(self):
        if self.selected_movie:
            return [date for date in self.movies_dict[self.selected_movie].keys()]
        else:
            raise ValueError('Nie wybrano filmu! Pierw należy wybrać tytuł filmu!')

    @property
    def hours_selected_movie(self):
        if self.__selected_date:
            return [hour for hour in self.movies_dict[self.selected_movie][self.__selected_date].keys()]

    @property
    def titles(self):
        return [title for title in self.movies_dict.keys()]

    @property
    def selected_movie(self):
        return self.__selected_movie

    @property
    def selected_date(self):
        return self.__selected_date

    @property
    def __len_dates(self) -> len:
        return len(self.dates_selected_movie)

    @property
    def __len_hours(self) -> len:
        return len([self.movies_dict[self.selected_movie][self.__selected_date]])

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        self.__mode = value

    def get_movie_by_index(self, index: str) -> str | None:
        if index in ['Z', 'z']:
            self.__mode = -1
            return index
        index = int(index)
        if 0 < index <= len(self.titles):
            self.__selected_movie = self.titles[index - 1]
        else:
            print('Index wykracza poza zakres danych!')

    def get_date_by_index(self, index: str) -> str | None:
        if index in['Z', 'z']:
            self.__mode = -1
            return index
        index = int(index)
        if 0 < index <= self.__len_dates:
            self.__selected_date = self.dates_selected_movie[index - 1]
            return self.dates_selected_movie[index - 1]
        else:
            print('Index wykracza poza zakres danych!')

    def get_hour_by_index(self, index: str) -> str | None:
        if index in['Z', 'z']:
            self.__mode = -1
            return index
        index = int(index)
        if 0 < index <= self.__len_hours:
            self.__selected_hour = self.hours_selected_movie[index - 1]
            return self.dates_selected_movie[index - 1]
        else:
            print('Index wykracza poza zakres danych!')