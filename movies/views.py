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
    brought_movies = {}
    if request.method == "GET":
        def send_req_and_save():
            url = "https://api.themoviedb.org/3/movie/now_playing"
            for page_num in range(1, 10):
                params = {
                    "api_key" : secrets["API_KEY"],
                    "language" : "ko-KR",
                    "region" : "KR",
                    "page" : page_num
                }
                brought_movies = requests.get(url, params).json()["results"]
                print(brought_movies)
                for movie in brought_movies:
                    if Movie.objects.filter(overview=movie["overview"]):
                        continue
                    serializer = MovieSerializer(data=movie)
                    if serializer.is_valid():
                        serializer.save()
        send_req_and_save()
        movies = get_list_or_404(Movie)
        list_serializer = MovieSerializer(movies, many=True)
        return Response(list_serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":

    