from django.db import models

class Concert(models.Model):
    BOROUGH_CHOICES = [
        ('BK', 'Brooklyn'),
        ('MN', 'Manhattan'),
        ('BX', 'The Bronx'),
        ('QN', 'Queens'),
        ('SI', 'Staten Island')
    ]

    id = models.IntegerField(primary_key = True)
    datetime = models.DateTimeField()
    venue_name = models.CharField(max_length = 100)
    borough = models.CharField(max_length = 2, choices = BOROUGH_CHOICES)
    performer_names = models.CharField(max_length = 200)
    genres = models.CharField(max_length = 200)
    event_url = models.URLField()
    performer_image_url = models.URLField(null = True)

    def __str__(self):
        return self.performer_names + " at " + self.venue_name + " on " + str(self.datetime) + " in " + self.borough


class UserSignup(models.Model):
    username = models.CharField(max_length=20)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    dateOfBirth = models.DateField()
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username

class LoginUser(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    isValidated = models.BooleanField()
