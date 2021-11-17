from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from server.settings import BASE_DIR

from .models import Movie
from .serializers import MovieSerializer

import requests
# api 숨기기
import os, json, sys
SECRET_PATH = os.path.join(BASE_DIR, 'secrets.json')
secrets = json.loads(open(SECRET_PATH).read())
# Create your views here.
@api_view(['GET', 'POST'])
def index(request):
    '''
    GET : 현재 상영 영화 리스트 가져와 DB에 저장 후 전체 리스트 반환
    POST : 영화 추가
    '''
    if request.method == "GET":
        def send_req_and_save():
            url = "https://api.themoviedb.org/3/movie/now_playing"
            for page_num in range(1, 10):       # 1~10까지 페이지를 바꿔가며 요청
                params = {
                    "api_key" : secrets["API_KEY"], # secrets.json 파일에 숨겨둠
                    "language" : "ko-KR",
                    "region" : "KR",
                    "page" : page_num
                }
                brought_movies = requests.get(url, params).json()["results"]    # 요청으로 받아온 영화들

                for movie in brought_movies:                                    # 각 영화를 overview로 비교하여 겹치지 않는 경우 저장
                    if Movie.objects.filter(overview=movie["overview"]):
                        continue
                    serializer = MovieSerializer(data=movie)
                    if serializer.is_valid():
                        serializer.save()
        send_req_and_save()
        movies = get_list_or_404(Movie)                                         # DB에 저장된 모든 영화들 반환
        list_serializer = MovieSerializer(movies, many=True)
        return Response(list_serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    