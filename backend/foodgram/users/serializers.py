import base64

from rest_framework import serializers
from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model

from .models import Subscription
from recipes.models import Recipe

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
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = UserModel
        fields = ('email', 'id', 'username', 'first_name', 
                  'last_name', 'is_subscribed', 'avatar')
        
    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=user,
            following=obj
        ).exists()
    

class UserRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
    

class SubscriptionSerializer(MyUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(MyUserSerializer.Meta):
        fields = MyUserSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)

        request = self.context['request']
        recipes_limit = request.query_params.get('recipes_limit')

        try:
            recipes_limit = int(recipes_limit)
        except:
            recipes_limit = 0
        
        if recipes_limit > 0:
            recipes = recipes[:recipes_limit]

        serializer = UserRecipeSerializer(recipes, many=True)

        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
        