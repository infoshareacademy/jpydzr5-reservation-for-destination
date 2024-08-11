from cinema import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("cennik/", views.price_list, name="price_list"),
    path("repertuar/", views.repertoire, name="repertoire"),
    path("koszyk/", views.basket, name="basket"),
]
