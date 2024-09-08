from django.db import models


class User(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)


class Price(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)


class Seance(models.Model):
    show_start = models.DateTimeField()
    hall_number = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Reservation(models.Model):
    repertoire = models.ForeignKey(Seance, on_delete=models.CASCADE)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    row = models.CharField(max_length=1)
    seat = models.IntegerField()
