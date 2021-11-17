from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (  
                    "id",
                    "title",
                    "overview",
                    # genre_ids,
                    # director,
                    "adult",
                    "vote_average",
                    "popularity",
                    "release_date",
                    "poster_path",
                )
