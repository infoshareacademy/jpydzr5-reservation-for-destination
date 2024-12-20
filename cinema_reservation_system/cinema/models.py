import uuid
import pendulum
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta


class TicketType(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    extra_validation = models.BooleanField(default=True)
    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    duration = models.DurationField(default=timedelta(minutes=120))
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)

    def __str__(self):
        return self.title


class Cinema(models.Model):
    """Model reprezentujący kino."""
    name = models.CharField(max_length=100)  # Nazwa kina
    city = models.CharField(max_length=100)  # Miasto, w którym znajduje się kino

    def __str__(self):
        return f"{self.name} w {self.city}"


class Hall(models.Model):
    """Model reprezentujący salę kinową."""
    cinema = models.ForeignKey(Cinema, on_delete=models.RESTRICT)  # Powiązanie z modelem Cinema
    name = models.CharField(max_length=10)  # Numer sali
    cleaning_time = models.DurationField()  # Czas sprzątania

    def __str__(self):
        return f"Sala {self.name} w kinie {self.cinema.name}"


class Seance(models.Model):
    """Klasa reprezentująca seans,
    czyli pojedyncze wyświetlenie konkretnego filmu w konkretnej sali o konkretnej godzinie"""
    show_start = models.DateTimeField(default=pendulum.now)
    hall = models.ForeignKey(Hall, on_delete=models.RESTRICT, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.RESTRICT, null=True, related_name='seances')

    def __str__(self):
        return f'{self.movie.title} - {self.show_start} - {self.hall}'

    def clean(self):
        # Oblicz czas zakończenia tego seansu wraz z czasem sprzątania
        show_end_with_cleaning = self.show_start + self.movie.duration + self.hall.cleaning_time

        # Sprawdź inne seanse w tej samej sali
        overlapping_seances = Seance.objects.filter(
            hall=self.hall,
            show_start__lt=show_end_with_cleaning,
            show_start__gte=self.show_start
        ).exclude(pk=self.pk)

        if overlapping_seances.exists():
            raise ValidationError(
                f"Seans nachodzi na inny seans w tej samej sali. "
                f"Należy uwzględnić czas trwania filmu i sprzątania."
            )

    def save(self, *args, **kwargs):
        self.clean()  # Wywołaj walidację przed zapisem
        super().save(*args, **kwargs)


    @property
    def progress(self):
        now = pendulum.now()
        if self.show_start <= now <= self.show_start + self.movie.duration:
            elapsed_time = (now - self.show_start).total_seconds()
            progress = (elapsed_time / self.movie.duration.total_seconds()) * 100
            return min(100, round(progress)), 0

        if self.show_start + self.movie.duration <= now <= self.show_start + self.movie.duration + self.hall.cleaning_time:
            elapsed_time = (now - (self.show_start + self.movie.duration)).total_seconds()
            progress = (elapsed_time / self.hall.cleaning_time.total_seconds()) * 100
            return 100, min(100, round(progress))

        return 100,100 if now > self.show_start + self.movie.duration + self.hall.cleaning_time else 0,0

    @property
    def minutes_to_end(self):
        now = pendulum.now()
        return round((self.show_start + self.movie.duration - now).total_minutes())


class SeatType(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='media/icons/', null=True)
    allowed_ticket_types = models.ManyToManyField(TicketType, blank=True)  # Powiązanie z TicketType

    def __str__(self):
        return self.name


class Seat(models.Model):
    """Model reprezentujący miejsce w sali kinowej."""

    hall = models.ForeignKey(Hall, on_delete=models.RESTRICT)  # Powiązanie z modelem Hall
    pos_x = models.PositiveIntegerField()
    pos_y = models.PositiveIntegerField()
    rotation = models.FloatField(default=0)
    seat_type = models.ForeignKey(SeatType, on_delete=models.RESTRICT, null=True)
    row = models.CharField(max_length=2, null=True)
    column = models.CharField(max_length=3, null=True)

    def __str__(self):
        return (f"Miejsce o id {self.id} w sali {self.hall.name} "
                f"[{self.seat_type.name if self.seat_type else ''}])")
    
    @property
    def number(self):
        return f"{self.row}{self.column}"

class Reservation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    seance = models.ForeignKey(Seance, on_delete=models.RESTRICT, null=True)
    paid = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    used = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)


    @property
    def total_price(self):
        """Oblicza całkowitą cenę rezerwacji na podstawie wybranych biletów i miejsc."""
        total = 0
        for seat_reservation in self.seatreservation_set.all():
            total += seat_reservation.ticket_type.price
        return total

    @property
    def too_early(self):
        """Sprawdza, czy seans zaczyna się za mniej niż godzinę."""
        if not self.seance:
            return False

        return pendulum.now().add(hours=1) < self.seance.show_start

    @property
    def too_late(self):
        """Sprawdza, czy seans już się nie skończył."""
        if not self.seance:
            return False

        return self.seance.show_start + self.seance.movie.duration < pendulum.now().subtract(minutes=20)


class SeatReservation(models.Model):
    reservation = models.ForeignKey('Reservation', on_delete=models.RESTRICT, null=True)
    ticket_type = models.ForeignKey('TicketType', on_delete=models.RESTRICT)
    seat = models.ForeignKey('Seat', on_delete=models.RESTRICT)
    paid = models.BooleanField(default=False)  # Flaga, która może być użyteczna do późniejszych operacji
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Cena biletu

    def __str__(self):
        return f"{self.seat} - {self.ticket_type}"

    def clean(self):
        """Sprawdzenie, czy seat jest już zarezerwowane na dany seans"""
        if SeatReservation.objects.filter(seat=self.seat, reservation__seance=self.reservation.seance).exclude(
                id=self.id).exists():
            raise ValidationError(f"Miejsce {self.seat} jest już zarezerwowane na ten seans.")

        # Ustal cenę biletu, jeśli jeszcze nie została ustawiona
        if self.price is None:
            self.price = self.ticket_type.price  # Cena biletu zależna od typu biletu

    def save(self, *args, **kwargs):
        """Wywołanie metody clean przed zapisem"""
        self.clean()
        super().save(*args, **kwargs)
