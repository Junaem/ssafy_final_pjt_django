from django.db import models
from movies.models import Movie
# Create your models here.
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # Todo : user, likeuser
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title