from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from api import models


class MyCustomToken(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        return token
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.User
        fields = ['full_name','email', 'username', 'password', 'confirm_password', ]

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Password Fields Should Match!'})
        return attrs
    
    def create(self, validated_data):
        user = models.User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            full_name = validated_data['full_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

    def get_post_count(self, category):
        return category.posts.count()
    class Meta:
        model = models.Category
        fields = ['id', 'title', 'image', 'slug', 'post_count']


class AuthorSerializer(serializers.Serializer):
    views = serializers.IntegerField(default=0)
    posts = serializers.IntegerField(default=0)
    likes = serializers.IntegerField(default=0)
    bookmarks = serializers.IntegerField(default=0)

# here should be comments serializer
