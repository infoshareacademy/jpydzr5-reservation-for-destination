from django.contrib import admin
from .models import Repertoire, User, Reservation, Price

admin.site.register(Repertoire)
admin.site.register(User)
admin.site.register(Reservation)
admin.site.register(Price)
