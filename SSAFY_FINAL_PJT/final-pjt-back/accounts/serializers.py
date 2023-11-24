from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('pk',
              'username',
              'nickname',
              'email',
              'age',
              'money',
              'salary',
              'financial_products',
              'is_superuser')
