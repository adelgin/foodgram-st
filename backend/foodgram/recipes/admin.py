from django.contrib import admin

from .models import (Ingredient, Recipe, IngredientRecipe, Favorite,
                     ShoppingCart)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name', )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    search_fields = ('name', 'author__username', 'author__email')
    list_display = ('id', 'name', 'author__username', 'favorite_count')

    def favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()
    

@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    pass