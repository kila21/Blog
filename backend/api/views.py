from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny

# Create your views here.

from api import serializer as api_serializer
from api import models as api_models


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyCustomToken


class RegisterView(generics.CreateAPIView):
    queryset = api_models.User.objects.all()
    serializer_class = api_serializer.RegisterSerializer
    permission_classes = [AllowAny]

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.ProfileSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        user = api_models.User.objects.get(id=user_id)
        profile = api_models.Profile.objects.get(user=user)
        return profile