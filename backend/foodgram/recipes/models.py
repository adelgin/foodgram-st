from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)
    measurement_unit = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Ингредиент'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='recipes')
    text = models.TextField()
    cooking_time = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        verbose_name = 'Рецепт'
        ordering = ('-created_at', )

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredient_amount')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'],
                                    name='unique ingredient recipe')]

    def __str__(self):
        return f'{self.recipe} - {self.ingredient} {self.amount}' \
            f'{self.ingredient.measurement_unit}'


class Favorite(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        verbose_name = 'Избранное'
        ordering = ('-created_at', )
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique recipe in favorite')]

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user.username}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        verbose_name = 'Корзина'
        ordering = ('-created_at', )
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique recipe in shopping cart')]

    def __str__(self):
        return f'{self.recipe} в корзине у {self.user.username}'
