from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('<int:movie_pk>/', views.detail),
    path('<int:movie_pk>/like/', views.get_movie_like),
    path('like/', views.post_movie_like),
]