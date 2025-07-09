from django.shortcuts import render
from rest_framework import viewsets, permissions

from .models import Ingredient, Recipe, IngredientRecipe
from .serializers import IngredientSerializer
from .filters import IngredientFilter


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = (IngredientFilter, )
    search_fields = ('^name', )
    pagination_class = None
