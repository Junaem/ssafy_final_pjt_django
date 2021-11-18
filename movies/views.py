from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import Movie
from .serializers import MovieSerializer

import requests

from server.settings import BASE_DIR
import os, json


# 숨긴 api 가져오기 
SECRET_PATH = os.path.join(BASE_DIR, 'secrets.json')
secrets = json.loads(open(SECRET_PATH).read())


# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def index(request):
    '''
    GET : 현재 상영 영화 리스트 가져와 DB에 저장 후 전체 리스트 반환
    POST : 영화 추가
    '''
    if request.method == "GET":
        def req_and_save(req_to, page_range):
            url = "https://api.themoviedb.org/3/movie/"+req_to
            for page_num in range(1, page_range+1):       # 정해놓은 range까지 페이지를 바꿔가며 요청
                params = {
                    "api_key" : secrets["API_KEY"], # secrets.json 파일에 숨겨둠
                    "language" : "ko-KR",
                    "region" : "KR",
                    "page" : page_num
                }
                brought_movies = requests.get(url, params).json()["results"]    # 요청으로 받아온 영화들
                # movies_serializer = MovieSerializer(data=brought_movies, many=True)   # 한번에 many=True로 지정해 넣을 경우 하나라도 id값이 겹치면 저장 불가..
                # if movies_serializer.is_valid():
                #     movies_serializer.save()
                for movie in brought_movies:                                    # 각 영화를 id로 비교
                    if Movie.objects.filter(id=movie["id"]).exists():                    # 겹치면 update한 serializer 사용
                        old_movie = Movie.objects.get(id=movie["id"])
                        serializer = MovieSerializer(instance=old_movie, data=movie)
                    else:                                                       # 겹치지 않으면 새로운 serializer 사용
                        serializer = MovieSerializer(data=movie)
                    if serializer.is_valid():   
                        serializer.save()
        req_and_save("popular", 5)
        req_and_save("top_rated", 5)
        req_and_save("upcoming", 2)
        movies = Movie.objects.order_by("-popularity")                      # DB에 저장된 모든 영화들 popularity 내림차순으로 반환
        list_serializer = MovieSerializer(movies, many=True)
        return Response(list_serializer.data, status=status.HTTP_200_OK)

    # elif request.method == "POST":
    #     serializer = MovieSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data)
    
@api_view(['GET', 'PUT', 'DELETE'])
def detail(request, movie_pk):
    '''
    GET : 영화 디테일 보여주기
    PUT : 영화 수정
    DELETE : 영화 삭제
    '''
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == "GET":
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = MovieSerializer(instance=movie, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == "DELETE":
        title = movie.title
        movie.delete()
        message = movie.title + "가 정상적으로 삭제됐습니다."
        return Response(data=message, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def movie_like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user
    if not movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.add(user)
    else :
        movie.like_users.remove(user)