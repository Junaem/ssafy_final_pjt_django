from functools import partial
from operator import mod
from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.fields import NullBooleanField
from rest_framework import validators

User = settings.AUTH_USER_MODEL

class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    overview = models.TextField()
    # genre_ids = models.CharField(max_length=50)
    # director = models.CharField(max_length=50)
    adult = models.BooleanField(default=False)
    tmdb_vote_average = models.FloatField()
    tmdb_vote_count = models.IntegerField(default=0)
    popularity = models.FloatField()
    release_date = models.DateField()
    poster_path = models.CharField(max_length=100)
    backdrop_path = models.CharField(max_length=100, default='')
    runtime = models.IntegerField(null=True)
    genre = models.ManyToManyField(Genre, related_name='movie')

    like_users = models.ManyToManyField(User, through='Vote_rate', related_name='like_movies')

    def __str__(self):
        return self.title


class Vote_rate(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    movie = models.ForeignKey(Movie, on_delete=CASCADE)
    rate = models.IntegerField(null=True, validators=[MinValueValidator(0), MaxValueValidator(10)])
