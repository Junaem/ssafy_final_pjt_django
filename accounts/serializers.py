from rest_framework import serializers
from django.contrib.auth import get_user, get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta :
        model = User
        fields = (
            'username', 
            'password', 
            'like_movies', 
            'like_reviews',
            'followings',
            'followers',
            )
        read_only_fields = (
            'followings',
            'followers',
        )