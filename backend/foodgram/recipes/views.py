from rest_framework import viewsets, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Ingredient, Recipe, Favorite
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
    
    @action(methods=['post', 'delete'], detail=True, url_path='favorite',
            permission_classes=(permissions.IsAuthenticated, ))
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user

        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            Favorite.objects.create(user=user, recipe=recipe)

            serializer = UserRecipeSerializer(recipe)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        favorite = Favorite.objects.filter(user=user, recipe=recipe)

        if favorite.exists():
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
