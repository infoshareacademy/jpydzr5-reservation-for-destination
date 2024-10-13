from . import views
from django.urls import path


urlpatterns = [
    path("", views.index, name="index"),
    path("set_cinema", views.set_cinema, name="set_cinema"),
    path("ticket_types/", views.price_list, name="price_list"),
    path("repertoire/", views.repertoire, name="repertoire"),
    path("reservation/", views.reservation, name="reservation"),
    path("basket/", views.basket, name="basket"),
    path('select_movie/', views.select_movie, name='select_movie'),
    path('select_seance/<int:movie_id>/', views.select_seance, name='select_seance'),
    path('select_seats/<int:seance_id>/', views.select_seats, name='select_seats'),
    path('select_ticket_type/<int:reservation_id>/', views.select_ticket_type, name='select_ticket_type'),
]

