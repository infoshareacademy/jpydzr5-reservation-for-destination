from django.db import models


class Repertoire(models.Model):
    movie_title = models.CharField(max_length=100)
    show_date = models.CharField(max_length=10)
    show_hour = models.CharField(max_length=5)
    hall_number = models.IntegerField()
    movie_description = models.CharField(max_length=300)
    price = models.FloatField()

    def __str__(self):
        return self.movie_title


class User(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Reservation(models.Model):
    repertoire = models.ForeignKey(Repertoire, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    row = models.CharField(max_length=1)
    seat = models.IntegerField()

    def __str__(self):
        return f"Rezerwacja dla {self.user} na {self.repertoire}"
