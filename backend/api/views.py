from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.views import APIView, Response, status
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

class CategoryListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.CategorySerializer

    def get_queryset(self):
        return api_models.Category.objects.all()
    
class PostCategoryListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.PostSerializer

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = api_models.Category.objects.get(slug=category_slug)
        return api_models.Post.objects.filter(category=category)

class PostListApiView(generics.ListAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return api_models.Post.objects.all()

class PostDetailApiView(generics.RetrieveAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs['post_slug']
        post = api_models.Post.objects.get(slug=slug)
        post.views += 1
        post.save()
        return post

class LikePostApiView(APIView):
    def post(self, request):
        user_id = request.data['user_id']
        post_id = request.data['post_id']

        user = api_models.User.objects.get(user=user_id)
        post = api_models.Post.objects.get(post=post_id)

        if user in post.likes.all():
            post.likes.remove(user)
            return Response({'message': 'Post Disliked'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            api_models.Notification.objects.create(
                user=post.user,
                post=post,
                type='Like'
            )
            return Response({'message': 'Post Liked'}, status=status.HTTP_201_CREATED)