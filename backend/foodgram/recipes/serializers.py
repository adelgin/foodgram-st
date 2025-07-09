import base64

from rest_framework import serializers
from django.core.files.base import ContentFile

from .models import Ingredient, Recipe, IngredientRecipe
from users.serializers import MyUserSerializer

class RecipeBase64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), 
                               name='recipe.' + ext)
        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    author = MyUserSerializer(read_only=True)
    image = RecipeBase64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = '__all__'

