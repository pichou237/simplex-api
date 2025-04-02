from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from.serializers import UserRegisterSerializer
from.models import User
from django.contrib.auth import authenticate

# Create your views here.


class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": serializer.data,
            "message": "User created successfully"
        }, status=status.HTTP_201_CREATED)
    


