from typing import Reversible
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Comment, Review
from .serializers import CommentSerializer, ReviewSerializer
from django.views.decorators.csrf import csrf_exempt

from movies.models import Movie
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
@api_view(["GET", "POST"])
def index(request):
    '''
    GET : 전체 리뷰 리스트 보여주기
    POST : 리뷰 등록하기
    '''
    if request.method == "GET":
        reviews = get_list_or_404(Review)
        reviews_json = []
        for review in reviews:
            serializer = ReviewSerializer(review)
            rev_ser = serializer.data

            movie_title = get_object_or_404(Movie, id=review.movie_id).title
            rev_ser["movie_title"] = movie_title

            username = get_object_or_404(User, id=review.user_id).username
            rev_ser["username"] = username
            reviews_json.append(rev_ser)
        return Response(reviews_json)

    elif request.method == "POST":
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
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

    if request.method == "POST":
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, review_id=review_pk)
            review_serializer = ReviewSerializer(instance=review)
            return Response(review_serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == "GET":
        serializer = ReviewSerializer(review)
        review_json = serializer.data
        user_id = review_json.get('user')
        
        username = get_object_or_404(User, id=user_id).username
        review_json["username"] = username

        movie_title = get_object_or_404(Movie, id=review.movie_id).title
        review_json["movie_title"] = movie_title

        comment_list = []                                        # serizlizer를 뜯어서 코멘트 json들을 담은 리스트를 추가한 다음 한 번에 Response로 보낼거임
        for comment_id in review_json["comment_set"]:
            comment=get_object_or_404(Comment, id=comment_id)
            com_ser = CommentSerializer(comment)
            com_json = com_ser.data
            
            comment_username = get_object_or_404(User, id=comment.user_id).username
            com_json["username"] = comment_username
            comment_list.append(com_json)
        
        review_json["comments_data"] = comment_list
        print(review_json)
        return Response(review_json)

    elif request.user.id != review.user_id:
        return Response({"권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == "PUT":
        serializer = ReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            review_json = serializer.data

            comment_list = []                                        # serizlizer를 뜯어서 코멘트 json들을 담은 리스트를 추가한 다음 한 번에 Response로 보낼거임
            for comment_id in review_json["comment_set"]:
                comment=get_object_or_404(Comment, id=comment_id)
                com_ser = CommentSerializer(comment)
                comment_list.append(com_ser.data)
            
            review_json["comments_data"] = comment_list

            return Response(review_json)
            # return Response(serializer.data)

    elif request.method == "DELETE":
        title = review.title
        review.delete()
        message = title + "가 정상적으로 삭제되었습니다."
        return Response(data=message, status=status.HTTP_204_NO_CONTENT)

    

@api_view(["POST"])
def review_like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    user = request.user

    if not review.like_users.filter(pk=user.pk).exists():
        review.like_users.add(user)
    else :
        review.like_users.remove(user)
    serializer = ReviewSerializer(review)
    return Response(serializer.data)


@api_view(["PUT", "DELETE"])    # get 필요한가?
def comment(request, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.user.id != comment.user_id:
        return Response({"권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "PUT":
        serializer = CommentSerializer(instance=comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, review_id=review_pk)
            review_serializer = ReviewSerializer(instance=review)
            return Response(review_serializer.data)
    
    elif request.method == "DELETE":
        comment.delete()
        return Response(data="댓글이 정상적으로 삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)
