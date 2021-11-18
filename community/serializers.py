from rest_framework import serializers
from .models import Review, Comment

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
                    "id",
                    "user",
                    "movie",
                    "title",
                    "content",
                )
        read_only_fields = ('id',)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
                    "id",
                    "user",
                    "review",
                    "content",
               )
        read_only_fields = ('id',)