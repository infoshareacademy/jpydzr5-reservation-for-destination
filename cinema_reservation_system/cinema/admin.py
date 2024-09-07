from django.contrib import admin
from .models import Repertoire, User, Reservation, Price, Movie


@admin.register(Repertoire)
class RepertoireAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
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


from django.contrib import admin
from .models import Cinema, Room, Seat

admin.site.register(Cinema)
admin.site.register(Room)
admin.site.register(Seat)