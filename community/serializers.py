from rest_framework import serializers
from .models import Review, Comment
# from rest_framework.fields import CurrentUserDefault

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
                    "id",
                    # "user",
                    "movie",
                    "title",
                    "content",
                    "like_users",
                    "comment_set"
                )
        read_only_fields = ('id', 'user', 'like_users', 'comment_set')

    # def save(self):
    #     user = CurrentUserDefault() 
    #     movie = self.validated_data['movie']
    #     title = self.validated_data['title']
    #     content = self.validated_data['content']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
                    "id",
                    "user",
                    "review",
                    "content",
               )
        read_only_fields = ('id', 'user', 'review')

    # def save(self):
    #     user = CurrentUserDefault() 
    #     review = self.validated_data['review']
    #     content = self.validated_data['content']