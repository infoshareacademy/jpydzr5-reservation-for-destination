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

class Seance(models.Model):
    show_start = models.DateTimeField(default=timezone.now)
    hall_number = models.IntegerField()
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.movie.title} - Sala: {self.hall_number} - {self.show_start}'


class Reservation(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE)
    price = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    row = models.CharField(max_length=1)
    seat = models.IntegerField()


class Cinema(models.Model):
    """Model reprezentujący kino."""
    name = models.CharField(max_length=100)  # Nazwa kina
    city = models.CharField(max_length=100)  # Miasto, w którym znajduje się kino

    def __str__(self):
        return f"{self.name} w {self.city}"


class Room(models.Model):
    """Model reprezentujący salę kinową."""
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)  # Powiązanie z modelem Cinema
    room_number = models.CharField(max_length=10)  # Numer sali
    cleaning_time = models.DurationField()  # Czas sprzątania

    def __str__(self):
        return f"Sala {self.room_number} w kinie {self.cinema.name}"


class Seat(models.Model):
    """Model reprezentujący miejsce w sali kinowej."""
    STATUS_CHOICES = [
        ('niedostępne', 'Niedostępne'),
        ('uszkodzone', 'Uszkodzone'),
        ('dostępne', 'Dostępne'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Powiązanie z modelem Room
    row = models.CharField(max_length=5)  # Rząd
    column = models.CharField(max_length=5)  # Kolumna
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='dostępne')  # Stan

    def __str__(self):
        return f"Miejsce {self.row}-{self.column} w sali {self.room.room_number} ({self.get_status_display()})"








