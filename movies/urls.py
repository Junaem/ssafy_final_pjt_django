from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('<int:movie_pk>/', views.detail),
    path('like/', views.movie_like),
]