from rest_framework import serializers
from .models import Review, Comment

from movies.models import Movie
from django.contrib.auth import get_user_model

User = get_user_model()

class ReviewSerializer(serializers.ModelSerializer):

    movie_title = serializers.SerializerMethodField()
    def get_movie_title(self, obj):
        movie_id = obj.movie_id
        return Movie.objects.get(id=movie_id).title
         

    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        user_id = obj.user_id
        return User.objects.get(id=user_id).username


    class Meta:
        model = Review
        fields = (
                    "movie",
                    "title",
                    "content",

                    "id",
                    "user",
                    "like_users",
                    "created_at",
                    "updated_at",
                    "comment_set",

                    "movie_title",
                    "username",
                )
        read_only_fields = ('id', 'user', 'like_users', 'comment_set', 'created_at', 'updated_at')

    # def save(self):
    #     user = CurrentUserDefault() 
    #     movie = self.validated_data['movie']
    #     title = self.validated_data['title']
    #     content = self.validated_data['content']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
                    "content",

                    "id",
                    "user",
                    "review",
                    "created_at",
                    "updated_at"
               )
        read_only_fields = ('id', 'user', 'review', 'created_at', 'updated_at')

    # def save(self):
    #     user = CurrentUserDefault() 
    #     review = self.validated_data['review']
    #     content = self.validated_data['content']