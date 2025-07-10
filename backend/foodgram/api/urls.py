from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import MyUserViewSet
from recipes.views import IngredientViewSet, RecipeViewSet

router = DefaultRouter()
router.register('users', MyUserViewSet, basename='users')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
