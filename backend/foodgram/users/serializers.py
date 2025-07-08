import base64

from rest_framework import serializers
from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class AvatarBase64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), 
                               name='user_avatar.' + ext)
        return super().to_internal_value(data)


class MyUserSerializer(UserSerializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    avatar = AvatarBase64ImageField(required=False, allow_null=True)

    class Meta(UserSerializer.Meta):
        model = UserModel
        fields = ('email', 'id', 'username', 'first_name', 
                  'last_name', 'avatar')