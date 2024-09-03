from django.db import models

# Create your models here.

from django.db import models

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