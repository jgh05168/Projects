from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import UserSerializer
from .models import User


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def signout(request):
  request.user.delete()
  return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def profileUpdate(request, user_pk):
  user = get_object_or_404(User, pk=user_pk)
  serializer = UserSerializer(user, data=request.data)
  if serializer.is_valid(raise_exception=True):
    serializer.save()
  return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request, user_pk):
  users = get_list_or_404(User)
  serializer = UserSerializer(users, many=True)
  return Response(serializer.data)