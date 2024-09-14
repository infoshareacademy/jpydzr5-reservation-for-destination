from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta


class TicketType(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    duration = models.DurationField(default=timedelta(minutes=120))

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
    hall_number = models.CharField(max_length=10)  # Numer sali
    cleaning_time = models.DurationField()  # Czas sprzątania

    def __str__(self):
        return f"Sala {self.hall_number} w kinie {self.cinema.name}"


class Seance(models.Model):
    show_start = models.DateTimeField(default=timezone.now)
    hall = models.ForeignKey(Hall, on_delete=models.RESTRICT, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return f'{self.movie.title} - {self.show_start} - Sala: {self.hall}'


class SeatType(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='media/icons/', null=True)

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
        return f"Miejsce o id {self.id} w sali {self.hall.hall_number} [{self.seat_type.name if self.seat_type else ''}])"


class Reservation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    seance = models.ForeignKey(Seance, on_delete=models.RESTRICT, null=True)


class SeatReservation(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.RESTRICT, null=True)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.RESTRICT)
    seat = models.ForeignKey(Seat, on_delete=models.RESTRICT)
    paid = models.BooleanField(default=False)

