from django.core.validators import MinValueValidator
from django.db import models

from recipes.ingredients.models import Ingredient
from users.models import User


class Tag(models.Model):
    """Класс тегов"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=100,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        unique=True,
        max_length=200
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Класс рецептов"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=(
            MinValueValidator(1, 'Минимальное время приготовления - 1 минута'),
        )
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Картинка'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Список id тегов'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    def get_str_ingredients(self):
        return '\n'.join(
            [
                f'{ingredient.name} - {ingredient.ingredient_amount.filter(recipe=self.pk)[0].amount} '
                f'{ingredient.measurement_unit}'
                for ingredient in self.ingredients.all()
            ]
        )

    get_str_ingredients.short_description = 'Ингредиенты'

    def get_str_tags(self):
        return '\n'.join([tag.name for tag in self.tags.all()])

    get_str_tags.short_description = 'Теги'


class IngredientInRecipe(models.Model):
    """Промежуточный класс для связывания рецепта с ингредиентом и его количеством"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_amount',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_amount',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(1, 'Количество должно быть больше 0'),
        ),
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'
