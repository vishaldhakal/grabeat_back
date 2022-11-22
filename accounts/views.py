from django.shortcuts import render, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from .serializers import UserSerializer
from rest_framework.response import Response
from api.models import User


@api_view(["GET"])
def userlists(request):
    users = User.objects.all()
    users_serializer = UserSerializer(users, many=True)
    return Response(users_serializer.data)


@api_view(["GET"])
def addUser(request):
    try:
        datas = JSONParser().parse(request)
        bank = User.objects.create(
            first_name=datas["first_name"],
            last_name=datas["last_name"],
            username=datas["username"],
            password=datas["password"],
            user_type=datas["user_type"],
        )
        bank.save()
        return JsonResponse(
            {"success": "User Created Successfull"},
            status=status.HTTP_201_CREATED,
        )
    except:
        return JsonResponse(
            {"error": "Bank Addition Failed"}, status=status.HTTP_400_BAD_REQUEST
        )
