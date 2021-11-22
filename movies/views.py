from django.db.models.fields import NullBooleanField
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

import movies

from .models import Movie, Vote_rate, Genre
from .serializers import MovieSerializer, Vote_rateSerializer, GenreSerializer
import requests

from community.models import Review
from community.serializers import ReviewSerializer
from django.contrib.auth import get_user_model

from server.settings import BASE_DIR
import os, json


# 숨긴 api 가져오기 
SECRET_PATH = os.path.join(BASE_DIR, 'secrets.json')
secrets = json.loads(open(SECRET_PATH).read())

User = get_user_model()

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
                        saved_movie = serializer.save(tmdb_vote_average=movie["vote_average"], tmdb_vote_count=movie["vote_count"])
                        genre_ids = movie["genre_ids"]                          # 장르 데이터 가져와서 m:n 관계 형성
                        for genre_id in genre_ids:
                            genre = get_object_or_404(Genre, id=genre_id)
                            if not genre.movie.filter(id=saved_movie.id).exists():
                                genre.movie.add(saved_movie)

        def req_genre():
            url = "https://api.themoviedb.org/3/genre/movie/list"
            params = {
                "api_key" : secrets["API_KEY"],
                "language" : "ko-KR",
            }
            genres = requests.get(url, params).json()["genres"]
            for genre in genres:
                serializer = GenreSerializer(data=genre)
                if serializer.is_valid():
                    serializer.save()

        req_genre()
        req_and_save("popular", 3)
        req_and_save("top_rated", 5)
        req_and_save("upcoming", 1)
        movies = Movie.objects.order_by("-popularity")                      # DB에 저장된 모든 영화들 popularity 내림차순으로 반환
        list_serializer = MovieSerializer(movies, many=True)
        return Response(list_serializer.data[:20], status=status.HTTP_200_OK)

    # elif request.method == "POST":
    #     serializer = MovieSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data)
    
@api_view(['GET'])
def detail(request, movie_pk):
    '''
    GET : 영화 디테일 보여주기
    PUT(기능x) : 영화 수정
    DELETE(기능x) : 영화 삭제
    '''
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == "GET":

        url = "https://api.themoviedb.org/3/movie/"+str(movie_pk)           # runtime 받아오기
        params = {
            "api_key" : secrets["API_KEY"],
            "language" : "ko-KR"
            }
        new_movie = requests.get(url, params).json()
        serializer = MovieSerializer(instance=movie, data=new_movie)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    # elif request.method == "PUT":
    #     serializer = MovieSerializer(instance=movie, data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data)
    # elif request.method == "DELETE":
    #     title = movie.title
    #     movie.delete()
    #     message = movie.title + "가 정상적으로 삭제됐습니다."
    #     return Response(data=message, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_movie_like(request, movie_id):
    if not Vote_rate.objects.filter(user_id=request.user.id, movie_id=movie_id).exists():       # 평점이 없을때 응답
        return Response({}, status.HTTP_204_NO_CONTENT)
    vote_rate = get_object_or_404(Vote_rate, user_id=request.user.id, movie_id=movie_id)
    serializer = Vote_rateSerializer(vote_rate)
    return Response(serializer.data)

@api_view(['POST'])
def post_movie_like(request):
    movie_id = request.data.get('movie_id')
    movie = get_object_or_404(Movie, id=movie_id)
    if not movie.like_users.filter(pk=request.user.id).exists():
        serializer = Vote_rateSerializer(data=request.data)
    else :
        vote_rate = get_object_or_404(Vote_rate, user_id=request.user.id, movie_id=movie_id)
        if not request.data.get('rate'):
            vote_rate.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = Vote_rateSerializer(instance=vote_rate, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)

    serializer = MovieSerializer(movie)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def genre(request, genre_id):
    movies = Movie.objects.filter(genre=genre_id).order_by('-popularity')
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data[:20])

@api_view(['GET'])
def recommend_a(request):
    votes = Vote_rate.objects.filter(user_id=request.user.id)
    if votes.exists():
        preference = {}
        for vote in votes:
            movie_id = vote.movie_id
            rate = vote.rate
            movies_genres = Genre.objects.filter(movie=movie_id)
            for genre in movies_genres:
                genre_id = genre.id
                if preference.get(genre_id):
                    preference[genre_id] += rate
                else :
                    preference[genre_id] = rate
        rank = sorted(preference, key= lambda x: -preference[x])
        preference["rank"] = rank
        return Response(preference)
    return Response({28:0, 35:0, 53:0, 16:0, 10749:0, "rank":[35, 53, 16, 10749, 28]})

@api_view(['GET'])
def classic(request):
    movies = Movie.objects.order_by('-tmdb_vote_average')
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data[:20])
    

@api_view(['GET'])
def new_movies(request):
    movies = Movie.objects.order_by('-release_date')
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data[:20])


@api_view(['GET'])
def watched(request):
    votes = Vote_rate.objects.filter(user_id=request.user.id).filter(rate__gte=6)
    watched_data=[]
    for vote in votes:
        movie = get_object_or_404(Movie, id=vote.movie_id)
        watched_data.append(MovieSerializer(movie).data)

    return Response(watched_data)