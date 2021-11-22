from rest_framework import serializers
from django.contrib.auth import get_user, get_user_model

from community.models import Review, Comment
from community.serializers import ReviewSerializer, CommentSerializer
from movies.models import Movie, Vote_rate
from movies.serializers import MovieSerializer, Vote_rate, Vote_rateSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta :
        model = User
        fields = (
            'id',
            'username', 
            'password', 
            'is_superuser'
            'like_movies', 
            'like_reviews',
            'followings',
            'followers',
            )
        read_only_fields = (
            'id',
            'like_movies',
            'like_reviews',
            'followings',
            'followers',
            'is_superuser'
        )

class UserProfileSerializer(serializers.ModelSerializer):

    reviews_data = serializers.SerializerMethodField()
    def get_reviews_data(self, obj):
        user_id = obj.id
        reviews = Review.objects.filter(user_id=user_id)
        return ReviewSerializer(reviews, many=True).data

    like_movies = serializers.SerializerMethodField()
    def get_like_movies(self, obj):
        user_id = obj.id
        vote_rates = Vote_rate.objects.filter(user_id=user_id)
        return Vote_rateSerializer(vote_rates, many=True).data


    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'followings',
            'followers',

            'is_superuser',

            'reviews_data',
            'like_movies',
        )
        read_only_fields = (
            'is_superuser',
        )