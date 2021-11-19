from rest_framework import serializers
from .models import Review, Comment
# from rest_framework.fields import CurrentUserDefault

class ReviewSerializer(serializers.ModelSerializer):
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