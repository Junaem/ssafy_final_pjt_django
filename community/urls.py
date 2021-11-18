from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('<int:review_pk>/', views.review_detail),
    # path('<int:review_pk>/<int:comment_pk>/', views.comment)
]