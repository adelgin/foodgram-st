import base64

from rest_framework import serializers
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator

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


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',
        required=True
    )
    name = serializers.CharField(source='ingredeint.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True)
    amount = serializers.IntegerField(
        validators=[MinValueValidator(limit_value=1), ], required=True)
    
    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = MyUserSerializer(read_only=True)
    image = RecipeBase64ImageField(required=True)
    cooking_time = serializers.IntegerField(
        validators=[MinValueValidator(limit_value=1), ], required=True)
    ingredients = IngredientRecipeSerializer(source='ingredient_amount', 
                                             required=True, many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'author', 'ingredients', 'name', 
                  'image', 'text', 'cooking_time']

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredient_amount')
        recipe = Recipe.objects.create(**validated_data)
        IngredientRecipe.objects.bulk_create([
            IngredientRecipe(
                recipe=recipe,
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount']) for ingredient in ingredients])
        return recipe
    
    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')

        if not ingredients:
            raise serializers.ValidationError('Ingredients can\'t be empty.')
        
        seen_ingredients = []

        for ingredient in ingredients:
            if ingredient['id'] in seen_ingredients:
                raise serializers.ValidationError(
                    'Ingredients must be unique.')
            seen_ingredients.append(ingredient['id'])

        return data
