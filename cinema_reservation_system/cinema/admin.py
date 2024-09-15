from django.contrib import admin
from . import models


@admin.register(models.Seance)
class RepertoireAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SeatReservation)
class ReservationSeatAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')  # Możesz dostosować pola, które będą wyświetlane w panelu admina


@admin.register(models.Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('cinema', 'hall_number', 'cleaning_time')  # Pola do wyświetlania


@admin.register(models.Seat)
class SeatAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SeatType)
class SeatTypeAdmin(admin.ModelAdmin):
    pass
