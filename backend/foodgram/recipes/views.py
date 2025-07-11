from rest_framework import viewsets, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (Ingredient, Recipe, Favorite, ShoppingCart,
                     IngredientRecipe)
from .serializers import IngredientSerializer, RecipeSerializer
from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthorOrReadOnly
from .pagination import RecipePaginator
from users.serializers import UserRecipeSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = (IngredientFilter, )
    search_fields = ('^name', )
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly, )
    pagination_class = RecipePaginator
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['get', ], detail=True, url_path='get-link')
    def get_short_link(self, request, pk):
        short_link = 'http://' + request.get_host() + '/recipes/' + pk
        return Response({'short-link': short_link}, status=status.HTTP_200_OK)

    def recipe_control(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user

        if request.method == 'POST':
            if model.objects.filter(user=user, recipe=recipe).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)

            model.objects.create(user=user, recipe=recipe)
            serializer = UserRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        object = model.objects.filter(user=user, recipe=recipe)

        if object.exists():
            object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post', 'delete'], detail=True, url_path='favorite')
    def favorite(self, request, pk):
        return self.recipe_control(Favorite, request, pk)

    @action(methods=['post', 'delete'], detail=True, url_path='shopping_cart')
    def shopping_cart(self, request, pk):
        return self.recipe_control(ShoppingCart, request, pk)

    @action(methods=['get', ], detail=False, url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        user = request.user
        recipes = Recipe.objects.filter(shoppingcart__user=user)

        ingredients = dict()

        for recipe in recipes:
            ingredient_in_recipe = IngredientRecipe.objects.filter(
                recipe=recipe).values('ingredient__name', 'amount',
                                      'ingredient__measurement_unit')
            for ingredient in ingredient_in_recipe:
                name = ingredient['ingredient__name']
                amount = ingredient['amount']
                measurement_unit = ingredient['ingredient__measurement_unit']
                if name not in ingredients.keys():
                    ingredients[name] = [0, measurement_unit]
                    print(ingredients[name][0])
                ingredients[name][0] += amount

        ingredients_list = [f'{name} - {value[0]} {value[1]}'
                            for name, value in ingredients.items()]

        ingredients_string = '\n'.join(ingredients_list)

        return FileResponse(ingredients_string, filename='shopping-list.txt',
                            as_attachment=True, content_type='text/plain')
