from django.core.validators import MinValueValidator
from django.db import models


class Ingredient(models.Model):
    """Класс ингредиентов"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )

    class Meta:
        pass

    def __str__(self):
        return self.name

    # class IngredientInRecipe(models.Model):
    """Промежуточный класс для связывания рецепта с ингредиентом и его количеством"""
    # recipe = models.ForeignKey(
    #     Recipe,
    #     on_delete=models.CASCADE,
    #     related_name='ingredient_amount',
    #     verbose_name='Рецепт'
    # )
    # ingredient = models.ForeignKey(
    #     Ingredient,
    #     on_delete=models.CASCADE,
    #     related_name='ingredient_amount',
    #     verbose_name='Ингредиент'
    # )
    # amount = models.PositiveSmallIntegerField(
    #     validators=[(
    #         MinValueValidator(1, 'Количество должно быть больше 0'),
    #     )],
    #     verbose_name='Количество',
    # )
    #
    # class Meta:
    #     verbose_name = 'Количество ингредиента'
    #     verbose_name_plural = 'Количество ингредиентов'
    #
    # def __str__(self):
    #     return f'{self.ingredient} {self.recipe}'
