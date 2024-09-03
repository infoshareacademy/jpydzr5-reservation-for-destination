from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Cinema, Room, Seat

admin.site.register(Cinema)
admin.site.register(Room)
admin.site.register(Seat)