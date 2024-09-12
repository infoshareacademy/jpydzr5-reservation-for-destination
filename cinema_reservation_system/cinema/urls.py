from . import views
from django.urls import path


urlpatterns = [
    path("", views.index, name="index"),
    path("cennik/", views.price_list, name="price_list"),
    path("repertuar/", views.repertoire, name="repertoire"),
    path("koszyk/", views.basket, name="basket"),
    path('select_seance/', views.select_seance, name='select_seance'),
    path('select_ticket/', views.select_ticket, name='select_ticket'),
]

