from System_of_reservation_tickets.price_list import PriceList
from menu import Menu
from repertoire import Repertoire
from cinema_hall import CinemaHall


def is_user_opt_out(checked_obj, checked_menu: Menu) -> bool:
    if checked_obj.mode == -1:
        checked_menu.option = '0'
        checked_obj.mode = '0'
        return True
    return False


if __name__ == '__main__':
    cinema_hall = CinemaHall(5, 10)
    repertoire = Repertoire(cinema_hall)
    menu = Menu()
    while menu.option != '4':
        print(menu)
        menu.option = input('Wybierz opcję: ')
        if menu.option not in ['0', '4']:
            match menu.option:
                case '1':
                    price_list = PriceList()
                    print(price_list)
                    user_input = repertoire.choose_seat(input('(z)rezygnuj: '))
                    if is_user_opt_out(repertoire, menu):
                        continue
                case '2':
                    menu.get_object_to_present(repertoire)
                    print(menu)
                    temp_index = input('Wybierz film lub (z)rezygnuj: ')
                    movie_title = repertoire.get_movie_by_index(temp_index)
                    if is_user_opt_out(repertoire, menu):
                        continue
                    print(menu)
                    temp_index = input('Wybierz datę lub (z)rezygnuj: ')
                    movie_date = repertoire.get_date_by_index(temp_index)
                    if is_user_opt_out(repertoire, menu):
                        continue
                    print(menu)
                    temp_index = input('Wybierz godzinę lub (z)rezygnuj: ')
                    movie_hour = repertoire.get_hour_by_index(temp_index)
                    print(menu)
                    temp_row = repertoire.choose_row(input('Wybierz rząd lub (z)zrezygnuj: '))
                    if is_user_opt_out(repertoire, menu):
                        continue
                    temp_seat = repertoire.choose_seat(input('Wybierz miejsce lub (z)rezygnuj: '))
                    if is_user_opt_out(repertoire, menu):
                        continue
                    repertoire.get_cinema_hall_by_movie_date_hour(
                        movie_title,
                        movie_date,
                        movie_hour
                    ).book_seat(temp_row, temp_seat)
        if menu.option == '4':
            break
        menu.option = '0'
