from csvGenerator import CSVGenerator
from menu import Menu
from repertoire import Repertoire
from cinema_hall import CinemaHall


def is_user_opt_out(checked_obj, checked_menu: Menu) -> bool:
    if checked_obj.mode == -1:
        checked_menu.option = '0'
        return True
    return False


if __name__ == '__main__':
    generator = CSVGenerator()
    generator.check_database_date()
    repertoire = Repertoire()
    cinema_hall = CinemaHall(5, 10)
    menu = Menu()
    while menu.option != '4':
        print(menu)
        menu.option = input('Wybierz opcję: ')
        if menu.option not in ['0', '4']:
            match menu.option:
                case '2':
                    repertoire = Repertoire()
                    menu.get_object_to_present(repertoire)
                    print(menu)
                    repertoire.get_movie_by_index(input())
                    if is_user_opt_out(repertoire, menu):
                        continue
                    repertoire.mode = 1
                    print(menu)
                    repertoire.get_date_by_index(input())
                    if is_user_opt_out(repertoire, menu):
                        continue
                    repertoire.mode = 2
                    print(menu)
                    repertoire.get_hour_by_index(input())
                    repertoire.mode = 3
                    menu.get_object_to_present(cinema_hall)
                    print(menu)
                    row = input('Wybierz rząd lub (z)rezygnuj: ')
                    if row in ['Z', 'z']:
                        cinema_hall.mode = -1
                    if is_user_opt_out(cinema_hall, menu):
                        continue
                    seat = input('Wybirz miejsce lub (z)rezygnuj: ')
                    if seat in ['Z', 'z']:
                        cinema_hall.mode = -1
                    if is_user_opt_out(cinema_hall, menu):
                        continue
                    cinema_hall.reserve_seat(row, seat)

        if menu.option == '4':
            break
        menu.option = '0'
