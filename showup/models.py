from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from dateutil.relativedelta import relativedelta


class Genre(models.Model):
    genre = models.TextField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["genre"], name="Genre_unique")]

    def __str__(self):
        return self.genre


class Concert(models.Model):
    BOROUGH_CHOICES = [
        ("BK", "Brooklyn"),
        ("MN", "Manhattan"),
        ("BX", "The Bronx"),
        ("QN", "Queens"),
        ("SI", "Staten Island"),
    ]

    id = models.IntegerField(primary_key=True)
    datetime = models.DateTimeField()
    venue_name = models.TextField()
    borough = models.TextField(choices=BOROUGH_CHOICES)
    performer_names = models.TextField()
    genres = models.ManyToManyField(Genre, related_name="genres", blank=True)
    event_url = models.URLField(max_length=100000)
    performer_image_url = models.URLField(max_length=100000, null=True)

    def __str__(self):
        return (
            f"{self.performer_names} at {self.venue_name}"
            f" on {str(self.datetime)} in {self.borough}"
        )


class Squad(models.Model):
    interested = models.ManyToManyField(Concert, related_name="interested", blank=True)
    going = models.ManyToManyField(Concert, related_name="going", blank=True)

    def __str__(self):
        return str(self.id)


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, blank=True)
    bio = models.TextField(max_length=500, default="", blank=True)
    swipes = models.ManyToManyField("self", through="Swipe", symmetrical=False)
    genres = models.ManyToManyField(Genre, related_name="fav_genres", blank=True)
    squad = models.ForeignKey(
        Squad, null=True, on_delete=models.CASCADE, related_name="squad"
    )

    def __str__(self):
        return self.email

    def get_age(self):
        return relativedelta(date.today(), self.date_of_birth).years


class Swipe(models.Model):
    swiper = models.ForeignKey(Squad, on_delete=models.CASCADE, related_name="swiper")
    swipee = models.ForeignKey(Squad, on_delete=models.CASCADE, related_name="swipee")
    event = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name="event")
    direction = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["swiper", "swipee", "event"],
                name=(
                    "You can only swipe on another particular person for a"
                    "particular event once."
                ),
            )
        ]

    def __str__(self):
        return (
            f"Swiper: {self.swiper.id}, "
            f"Swipee: {self.swipee.id}, "
            f"Event: {self.event.id}, "
            f"Direction: {self.direction}"
        )


class Request(models.Model):
    requester = models.ForeignKey(
        Squad, on_delete=models.CASCADE, related_name="requester"
    )
    requestee = models.ForeignKey(
        Squad, on_delete=models.CASCADE, related_name="requestee"
    )

    def __str__(self):
        return f"requester: {self.requester.id} requestee: {self.requestee.id}"
