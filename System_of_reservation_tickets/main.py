from menu import Menu

if __name__ == '__main__':
    menu = Menu()
    while menu.option != '4':
        print(menu)
        menu.option = input('Wybierz opcję: ')
        print(menu)
        if menu.option == '4':
            break
        menu.option = '0'
