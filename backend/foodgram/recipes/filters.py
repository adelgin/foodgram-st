from rest_framework.filters import SearchFilter
from django_filters import FilterSet

from .models import Recipe

class IngredientFilter(SearchFilter):
    search_param = 'name'

class RecipeFilter(FilterSet):
    class Meta:
        model = Recipe
        fields = ('author', )

