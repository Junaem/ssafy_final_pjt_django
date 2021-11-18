from operator import mod
from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import validators

User = settings.AUTH_USER_MODEL

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    overview = models.TextField()
    # genre_ids = models.CharField(max_length=50)
    # director = models.CharField(max_length=50)
    adult = models.BooleanField(default=False)
    tmdb_vote_average = models.FloatField()
    popularity = models.FloatField()
    release_date = models.DateField()
    poster_path = models.CharField(max_length=200)

    like_users = models.ManyToManyField(User, through='Vote_rate', related_name='like_movies')

    def __str__(self):
        return self.title


class Vote_rate(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    movie = models.ForeignKey(Movie, on_delete=CASCADE)
    rate = models.IntegerField(null=True, validators=[MinValueValidator(0), MaxValueValidator(10)])