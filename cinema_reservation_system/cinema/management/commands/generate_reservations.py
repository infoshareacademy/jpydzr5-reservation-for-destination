import pendulum
import random
import sys

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from cinema import models
from tqdm import tqdm


class Command(BaseCommand):
    help = "Wygeneruj rezerwacje"

    def handle(self, *args, **kwargs):

        today = pendulum.today()
        seances = models.Seance.objects.filter(show_start__gt=today.subtract(days=7))

        user = User.objects.get(pk=2)  # Użytkownik testowy
        ticket_type = models.TicketType.objects.get(pk=1)  # Normalny bilet

        for seance in tqdm(seances, file=sys.stdout, desc="Seance Processing"):
            reservation = models.Reservation.objects.create(
                user=user,
                seance=seance,
                paid=random.choice([True, False]),
            )

            possible_seats = seance.hall.seat_set.all()
            if possible_seats.count() > 10:
                min_seats = 10
            else:
                min_seats = 0

            for _ in range(random.randint(10, possible_seats.count())):
                try:
                    models.SeatReservation.objects.create(
                        reservation=reservation,
                        ticket_type=ticket_type,
                        seat=random.choice(possible_seats),
                    )
                except ValidationError:
                    # jeśli się wywali, to trudno - znaczy duplikat był i nie można zarezerwować
                    pass
