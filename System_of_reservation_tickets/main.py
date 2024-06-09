from Menu import Menu

if __name__ == '__main__':
    menu = Menu()
    print(menu)
    option = None
    while option != '5':
        option = menu.choose_option()
        if option != '5':
            print(menu)
