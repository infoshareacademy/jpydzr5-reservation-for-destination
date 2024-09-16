from . import views
from django.urls import path


urlpatterns = [
    path("", views.index, name="index"),
    path("cennik/", views.price_list, name="price_list"),
    path("repertuar/", views.repertoire, name="repertoire"),
    path("koszyk/", views.basket, name="basket"),
    path('select_movie/', views.select_movie, name='select_movie'),
    path('select_seance/<int:movie_id>/', views.select_seance, name='select_seance'),
    path('select_seats/<int:seance_id>/', views.select_seats, name='select_seats'),
    path('select_ticket_type/<int:reservation_id>/', views.select_ticket_type, name='select_ticket_type'),
]

