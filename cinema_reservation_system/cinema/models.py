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


class Repertoire(models.Model):
    show_date = models.CharField(max_length=10)
    show_hour = models.CharField(max_length=5)
    hall_number = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Reservation(models.Model):
    repertoire = models.ForeignKey(Repertoire, on_delete=models.CASCADE)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    row = models.CharField(max_length=1)
    seat = models.IntegerField()
