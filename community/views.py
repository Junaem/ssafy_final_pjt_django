from typing import Reversible
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Comment, Review
from .serializers import CommentSerializer, ReviewSerializer
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@api_view(["GET", "POST"])
def index(request):
    '''
    GET : 전체 리뷰 리스트 보여주기
    POST : 리뷰 등록하기
    '''
    if request.method == "GET":
        reviews = get_list_or_404(Review)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET", "POST", "PUT", "DELETE"])
def review_detail(request, review_pk):
    '''
    GET : 리뷰 내용 보여주기
    POST : 댓글 달기
    PUT : 리뷰 수정하기
    DELETE : 리뷰 지우기
    '''
    review = get_object_or_404(Review, id=review_pk)
    if request.method == "GET":
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == "DELETE":
        title = review.title
        review.delete()
        message = + title + "가 정상적으로 삭제되었습니다."
        return Response(data=message, status=status.HTTP_204_NO_CONTENT)

    elif request.method == "POST":
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            review_serializer = ReviewSerializer(instance=review)
            return Response(review_serializer.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def review_like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    user = request.user

    if not review.like_users.filter(pk=user.pk).exists():
        review.like_users.add(user)
    else :
        review.like_users.remove(user)


@api_view(["PUT", "DELETE"])    # get 필요한가?
def comment(request, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == "PUT":
        serializer = CommentSerializer(instance=comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            review_serializer = ReviewSerializer(instance=review)
            return Response(review_serializer.data)
    
    elif request.method == "DELETE":
        comment.delete()
        return Response(data="댓글이 정상적으로 삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)
