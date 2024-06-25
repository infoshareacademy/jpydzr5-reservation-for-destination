from csvGenerator import CSVGenerator
from menu import Menu

if __name__ == '__main__':
    generator = CSVGenerator()
    generator.check_database_date()
    menu = Menu()
    print(menu)
    while menu.option != '4':
        menu.option = input('Wybierz opcję: ')
        if menu.option not in ['0', '4']:
            print(menu)
        if menu.option == '4':
            break
        menu.option = '0'
        print(menu)
