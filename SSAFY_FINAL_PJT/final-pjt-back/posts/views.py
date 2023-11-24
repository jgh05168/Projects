from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model

from .serializers import PostListSerializer, PostSerializer, CategorySerializer, CommentSerializer, UserSerializer
from .models import Category, Post, Comment


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_list(request):
  if request.method == 'GET':
    posts = Post.objects.all()
    if not posts:
      return Response([])
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    serializer = PostSerializer(data=request.data)
    category = get_object_or_404(Category, pk=request.data['category'])
    if serializer.is_valid(raise_exception=True):
      serializer.save(category=category, user=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category(request):
  if request.method == 'GET':
    category = get_list_or_404(Category)
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def category_create(request):
  if request.method == 'POST':
    user = UserSerializer(request.user).data
    if user['is_superuser']:
      serializer = CategorySerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def category_delete(request, category_pk):
  category = get_object_or_404(Category, pk=category_pk)
  category.delete()
  return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def post_detail(request, post_pk):
  post = get_object_or_404(Post, pk=post_pk)
  if request.method == 'GET':
    serializer = PostSerializer(post)
    return Response(serializer.data)
  
  elif request.method == 'DELETE':
    if request.user == post.user:
      post.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
  
  elif request.method == 'PUT':
    if request.user == post.user:
      serializer = PostSerializer(post, data=request.data)
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment(request, post_pk):
  post = get_object_or_404(Post, pk=post_pk)
  if request.method == 'GET':
    comments = Comment.objects.filter(post=post)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
  
  elif request.method == 'POST':
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(post=post, user=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
  comment = get_object_or_404(Comment, pk=comment_pk)
  if request.method == 'DELETE':
    if request.user == comment.user:
      comment.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request, post_pk):
  post = get_object_or_404(Post, pk=post_pk)
  if request.user in post.like_users.all():
    post.like_users.remove(request.user)
  else:
    post.like_users.add(request.user)
  serializer = PostSerializer(post)
  return Response(serializer.data, status=status.HTTP_200_OK)