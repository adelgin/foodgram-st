from django.db import models

from django.contrib.auth import get_user_model

UserModel = get_user_model()

class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)
    measurement_unit = models.CharField(max_length=64)


class Recipe(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='recipes')
    text = models.TextField()
    cooking_time = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        ordering = ('-created_at', )


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredient_amount')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'],
                                    name='unique ingredient recipe')]

    
class Favorite(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        ordering = ('-created_at', )
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique recipe in favorite')]
        

class ShoppingCart(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        ordering = ('-created_at', )
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique recipe in shopping cart')]
