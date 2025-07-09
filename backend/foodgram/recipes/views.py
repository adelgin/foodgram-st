from django.shortcuts import render
from rest_framework import viewsets, permissions

from .models import Ingredient, Recipe, IngredientRecipe
from .serializers import IngredientSerializer, RecipeSerializer
from .filters import IngredientFilter
from .permissions import IsAuthorOrReadOnly
from .pagination import RecipePaginator


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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
