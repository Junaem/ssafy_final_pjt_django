from django.shortcuts import get_object_or_404
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer

from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    password = request.data.get('password')
    password_confirmation = request.data.get('password_confirmation')
    if password !=password_confirmation:
        return Response({'password': ['비밀번호 확인이 일치하지 않습니다.']}, HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(password)
        user.save()
        return Response(serializer.data, HTTP_201_CREATED)

@api_view(["GET"])
def profile(request, personname):
    person = get_object_or_404(User, username=personname)
    serializer = UserSerializer(person)
    return Response(serializer.data)

@api_view(["POST"])
def follow(request, personname):
    me = request.user
    you = get_object_or_404(User, username=personname)
    if me != you:
        if not me.followings.filter(username=personname).exists():
            me.followings.add(you)
        else:
            me.followings.remove(you)
    serializer = UserSerializer(you)
    return Response(serializer.data)