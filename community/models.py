from django.db import models
from django.db.models.deletion import CASCADE
from movies.models import Movie
from django.conf import settings


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # Todo : user, likeuser
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    review = models.ForeignKey(Review, on_delete=CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title