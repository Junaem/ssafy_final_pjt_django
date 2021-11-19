from rest_framework import serializers
from .models import Movie, Vote_rate
from rest_framework.fields import CurrentUserDefault

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
            "popularity",
            "release_date",
            "poster_path",

            "tmdb_vote_average",
            "like_users",
            "review_set",
            "runtime",
        )
        read_only_fields = ('like_users', 'tmdb_vote_average', 'review_set')

class Vote_rateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote_rate
        fields = (
            "movie_id",
            "rate",

            "user_id",
        )

        read_only_fields = ('user_id',)
    
    # def save(self):
    #     user = CurrentUserDefault()         # 유저 가져오기!!
    #     movie = self.validated_data['movie']
    #     rate = self.validated_data['rate']
