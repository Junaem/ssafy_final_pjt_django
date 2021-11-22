from rest_framework import serializers
from .models import Movie, Vote_rate, Genre
from rest_framework.fields import CurrentUserDefault

from community.models import Review
from community.serializers import ReviewSerializer

from django.db.models import Avg


class MovieSerializer(serializers.ModelSerializer):

    our_rate = serializers.SerializerMethodField()
    def get_our_rate(self, obj):
        movie_id = obj.id
        avg_rate = Vote_rate.objects.filter(movie_id=movie_id).aggregate(Avg('rate'))
        return avg_rate

    # total_rate = serializers.SerializerMethodField()
    # def get_total_rate(self, obj):
    #     movie_id = obj.id
    #     vote_rate = Vote_rate.objects.filter(movie_id=movie_id)
    #     vote_pnt = vote_rate.aggregate


    reviews_data = serializers.SerializerMethodField()
    def get_reviews_data(self, obj):
        movie_id = obj.id
        reviews = Review.objects.filter(movie_id=movie_id)
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

    genre = serializers.SerializerMethodField()
    def get_genre(self, obj):
        movie_id = obj.id
        genres = Genre.objects.filter(movie=movie_id)
        serializer = GenreSerializer(genres, many=True)
        return serializer.data


    class Meta:
        model = Movie
        fields = (  
            "id",
            "title",
            "overview",
            
            "adult",
            "popularity",
            "release_date",
            "poster_path",
            "runtime",

            "tmdb_vote_average",
            "tmdb_vote_count",
            "like_users",
            "review_set",

            "our_rate",
            "reviews_data",
            "genre",            # 원래 있는 필드를 바꿀 수도 있나?
        )
        read_only_fields = ('like_users', 'tmdb_vote_average', 'tmdb_vote_count', 'review_set', 'genre')

class Vote_rateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote_rate
        fields = (
            "rate",
            "movie_id",
            "user_id",
        )

        read_only_fields = ('user_id',)
    
    # def save(self):
    #     user = CurrentUserDefault()         # 유저 가져오기!!
    #     movie = self.validated_data['movie']
    #     rate = self.validated_data['rate']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"
        