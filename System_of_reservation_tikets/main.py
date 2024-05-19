from Menu import Menu

if __name__ == '__main__':
    menu = Menu()
    print(menu)
    option = None
    while option != '5':
        option = menu.choose_option()
        print(menu)
