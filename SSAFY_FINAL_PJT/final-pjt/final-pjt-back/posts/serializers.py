from rest_framework import serializers
from .models import Category, Post, Comment
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ('pk', 'username', 'is_superuser')


class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  category = CategorySerializer(read_only=True)

  class Meta:
    model = Post
    fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  category = CategorySerializer(read_only=True)

  class CommentSerializer(serializers.ModelSerializer):
    class Meta:
      model = Comment
      fields = '__all__'

  comment_set = CommentSerializer(many=True, read_only=True)

  class Meta:
    model = Post
    fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  
  class Meta:
    model = Comment
    fields = '__all__'
    read_only_fields = ('post',)
