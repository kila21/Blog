from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 

from api import models


class MyCustomToken(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        return token
    
