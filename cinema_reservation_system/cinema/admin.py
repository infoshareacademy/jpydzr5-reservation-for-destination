from django.contrib import admin
from .models import Seance, Reservation, TicketType, Movie, Cinema, Hall, Seat


@admin.register(Seance)
class RepertoireAdmin(admin.ModelAdmin):
    pass


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')  # Możesz dostosować pola, które będą wyświetlane w panelu admina


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('cinema', 'hall_number', 'cleaning_time')  # Pola do wyświetlania


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('hall', 'row', 'column', 'status')  # Pola do wyświetlania
