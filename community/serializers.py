from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
                    "id",
                    "movie",
                    "title",
                    "content",
                )

class CommentSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
                    "id",
                    "user"
                    "review",
                    "content",
                )
