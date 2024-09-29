import pendulum
import random
import sys

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from cinema import models
from tqdm import tqdm


class Command(BaseCommand):
    help = "Wygeneruj seanse"

    def add_arguments(self, parser):
        # add optional or positional argument
        parser.add_argument('--max_seances',
                            default=50,
                            type=int,
                            help='how many seances should be generated?')
        parser.add_argument('--days_ahead',
                            default=7,
                            type=int,
                            help='how many days ahead should be generated?')

    def handle(self, *args, **kwargs):
        max_seances = kwargs['max_seances']
        days_ahead = kwargs['days_ahead']
        show_start = pendulum.time(10, 0)
        last_show = pendulum.time(22, 0)

        movies = models.Movie.objects.all()
        halls = models.Hall.objects.all()

        current_time = pendulum.time(show_start.hour, show_start.minute)
        last_show_time = pendulum.time(last_show.hour, last_show.minute)

        available_times = []

        while current_time <= last_show_time:
            available_times.append(current_time)
            current_time = current_time.add(minutes=15)

        # Generujemy max_seances liczby losowych seansów
        for _ in tqdm(range(max_seances), file=sys.stdout, desc = 'Generating seances'):
            hall = random.choice(halls)
            movie = random.choice(movies)

            # Losujemy dzień z zakresu od dziś do dziś + days_ahead
            today = pendulum.today()
            random_day = today.add(days=random.randint(0, days_ahead))

            # Losujemy godzinę z dostępnych
            random_time = random.choice(available_times)

            # Tworzymy pełny datetime dla wylosowanego dnia i godziny
            show_start = random_day.set(hour=random_time.hour, minute=random_time.minute)

            try:
                models.Seance.objects.create(
                    movie=movie,
                    hall=hall,
                    show_start=show_start,
                )
            except ValidationError:
                # wylosowany film nakłada się na inny, olewamy to
                pass
