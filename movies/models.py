from operator import mod
from django.db import models
from django.conf import settings

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    # genre_ids = models.CharField(max_length=50)
    # director = models.CharField(max_length=50)
    adult = models.BooleanField(default=False)
    vote_average = models.FloatField()
    popularity = models.FloatField()
    release_date = models.DateField()
    poster_path = models.CharField(max_length=200)

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_movies")

    def __str__(self):
        return self.title