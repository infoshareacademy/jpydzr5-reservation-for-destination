import random
from datetime import datetime, timedelta

from database_manager import DatabaseManager
from price_list import PriceList


class RepertoireGenerator:
    MOVIES = [
        {
            "title": "Avengers: Endgame",
            "description": "Ostateczne starcie superbohaterów Marvela z Thanossem, który zniszczył połowę wszechświata. Bohaterowie, pełni odwagi i poświęcenia, próbują naprawić zniszczenia i przywrócić harmonię. Widowiskowe efekty specjalne i emocjonalne pożegnania.",
        },
        {
            "title": "The Godfather",
            "description": "Epicka saga rodziny mafijnej Corleone, której głową jest Vito Corleone, budujący swoje imperium w brutalnym świecie przestępczym. Film o władzy, lojalności, zemście i rodzinie, uznawany za jedno z największych dzieł kinematografii.",
        },
        {
            "title": "Inception",
            "description": "Trzymający w napięciu thriller sci-fi o Domie Cobb, specjalizującym się w kradzieży tajemnic z umysłów ludzi poprzez sny. Film łączy wartką akcję z filozoficznymi pytaniami o rzeczywistość, pamięć i podświadomość, zaskakując widza na każdym kroku.",
        },
        {
            "title": "The Shawshank Redemption",
            "description": "Historia Andy'ego Dufresne'a, niesłusznie skazanego na dożywocie, który dzięki inteligencji, przyjaźni z Redem i niezłomnej nadziei, odnajduje w więzieniu swoją drogę do wolności. Film o triumfie ducha ludzkiego w najcięższych warunkach.",
        },
        {
            "title": "The Dark Knight",
            "description": "Batman walczy z Jokerem, szalonym geniuszem zbrodni, który zagraża bezpieczeństwu Gotham. Film ukazuje moralne dylematy bohatera i napięcie między dobrem a złem, z niezapomnianą rolą Heatha Ledgera jako Jokera. Mroczna, głęboka opowieść.",
        },
        {
            "title": "Pulp Fiction",
            "description": "Arcydzieło Quentina Tarantino, splatające losy płatnych zabójców, boksera i gangstera w pełnym ironii i przemocy świecie. Kultowe dialogi, niechronologiczna narracja i wyjątkowy styl uczyniły z tego filmu klasykę, która na stałe wpisała się w historię kina.",
        },
        {
            "title": "Forrest Gump",
            "description": "Opowieść o niezwykłym życiu Forresta Gumpa, prostego człowieka, który przypadkowo staje się świadkiem i uczestnikiem kluczowych wydarzeń w historii USA. To historia o miłości, niewinności i sile przypadku, pełna humoru i wzruszeń.",
        },
        {
            "title": "The Matrix",
            "description": "Neo odkrywa, że świat, w którym żyje, to tylko symulacja stworzona przez maszyny, kontrolujące ludzkość. Wraz z grupą rebeliantów podejmuje walkę o wolność. Przełomowe efekty specjalne, filozoficzne refleksje i kultowy styl uczyniły ten film ikoną popkultury.",
        },
        {
            "title": "Schindler's List",
            "description": "Wstrząsający dramat o Oskarze Schindlerze, który ratuje ponad tysiąc Żydów przed zagładą w czasie II wojny światowej. To przejmująca opowieść o ludzkiej godności, bohaterstwie i koszmarze Holokaustu, pozostawiająca widza w głębokiej refleksji.",
        },
        {
            "title": "Titanic",
            "description": "Epicka historia miłości Jacka i Rose, rozgrywająca się na tle jednej z największych katastrof morskich w historii. Film ukazuje nie tylko tragiczny rejs Titanica, ale także społeczne nierówności i siłę uczucia, które przetrwa nawet najgorsze przeciwności losu.",
        },
    ]
    SHOW_HOURS = ["10:00", "13:30", "16:45", "19:30", "22:15"]
    HALL_NUMBERS = ["1"]
    DAYS_NUMBERS = 7

    def __generate_show_dates(self):
        today = datetime.today()
        show_dates = [
            (today + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(self.DAYS_NUMBERS)
        ]
        return show_dates

    @staticmethod
    def __write_to_database(data: list):
        DatabaseManager.create_databases()
        DatabaseManager.add_repertoire(data)

    def prepare_data(self, last_showdate) -> None:
        # przygotowujemy daty na przyszły, aktualny tydzień
        today = datetime.today().date()
        start_date = last_showdate + timedelta(days=1)
        end_date = today + timedelta(days=self.DAYS_NUMBERS)

        next_week_show_dates = [
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((end_date - start_date).days + 1)
        ]

        # Generowanie 30 przykładowych danych seansów
        cinema_shows = [
            ["Movie_title", "Show_date", "Show_hour", "Hall_number", "Price"]
        ]
        price_list = PriceList()
        normal_price = price_list.get_price_by_name("Normalny")
        for _ in range(30):
            random_movie = random.choice(self.MOVIES)
            movie_title = random_movie["title"]
            movie_description = random_movie["description"]
            show_date = random.choice(next_week_show_dates)
            show_hour = random.choice(self.SHOW_HOURS)
            hall_number = random.choice(self.HALL_NUMBERS)
            price = normal_price
            cinema_shows.append(
                [
                    movie_title,
                    show_date,
                    show_hour,
                    hall_number,
                    movie_description,
                    price,
                ]
            )

        # Sortowanie danych według daty seansu i godziny seansu
        cinema_shows = sorted(cinema_shows[1:], key=lambda x: (x[1], x[2]))
        RepertoireGenerator.__write_to_database(cinema_shows)

    def check_repertoire_date(self):
        today = datetime.today().date()
        last_showdate_str = DatabaseManager.get_last_showdate_from_repertoire()

        # Pobieramy z bazy ostatnią date repertuaru i sprawdzamy, czy najpóźniejszy seans jest przynajmniej 7 dni
        # do przodu od dzisiejszej daty. Jeśli nie, wygenerujemy nowe seanse do 7 dni do przodu
        if last_showdate_str and datetime.strptime(
            last_showdate_str, "%Y-%m-%d"
        ).date() >= today + timedelta(days=self.DAYS_NUMBERS):
            print("Repertuar jest aktualny")
        else:
            print("Aktualizuję repertuar.")
            last_showdate = datetime.strptime(last_showdate_str, "%Y-%m-%d").date() if last_showdate_str else today
            self.prepare_data(last_showdate)
