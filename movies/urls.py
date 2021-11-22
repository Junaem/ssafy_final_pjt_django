from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('<int:movie_pk>/', views.detail),
    path('<int:movie_id>/like/', views.get_movie_like),
    path('like/', views.post_movie_like),
    path('genre/<int:genre_id>/', views.genre),
    path('classic/', views.classic),
    path('new_movies/', views.new_movies),
    path('watched/', views.new_movies),
    path('recommend_a/', views.recommend_a),

]