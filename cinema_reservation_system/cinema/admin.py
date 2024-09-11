from django.contrib import admin
from .models import Seance, Reservation, Price, Movie, Cinema, Room, Seat


@admin.register(Seance)
class RepertoireAdmin(admin.ModelAdmin):
    pass


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    pass


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')  # Możesz dostosować pola, które będą wyświetlane w panelu admina


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('cinema', 'room_number', 'cleaning_time')  # Pola do wyświetlania


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('room', 'row', 'column', 'status')  # Pola do wyświetlania
