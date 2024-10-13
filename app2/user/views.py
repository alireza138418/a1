# from django.shortcuts import render
# Create your views here

from rest_framework import generics
from .serializers import UserSerializers

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializers
