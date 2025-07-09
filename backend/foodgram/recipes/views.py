from django.shortcuts import render
from rest_framework import viewsets, permissions

from .models import Ingredient, Recipe, IngredientRecipe
from .serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = None
