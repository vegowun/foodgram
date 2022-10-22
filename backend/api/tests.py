from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from recipes.ingredients.models import Ingredient
from recipes.models import Recipe, IngredientInRecipe
from users.models import User


class IngredientViewSetTestCase(TestCase):
    def setUp(self) -> None:
        self.ingredient_1 = Ingredient.objects.create(
            name='Соль',
            measurement_unit='г.'
        )
        self.ingredient_2 = Ingredient.objects.create(
            name='Перец',
            measurement_unit='г.'
        )

    def check_object(self, data, obj):
        self.assertEqual(data.get('id'), obj.pk)
        self.assertEqual(data.get('name'), obj.name)

    def test_get_list(self):
        url = reverse('api:ingredients-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_detail(self):
        url = reverse('api:ingredients-detail', kwargs={'pk': self.ingredient_1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_object(response.data, self.ingredient_1)


class RecipeViewSetTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='auth')
        self.ingredient_1 = Ingredient.objects.create(
            name='Соль',
            measurement_unit='г.'
        )
        self.ingredient_2 = Ingredient.objects.create(
            name='Гречка',
            measurement_unit='г.'
        )

        self.recipe = Recipe.objects.create(
            name='Гречка с солью',
            author=self.user,
            cooking_time=20
        )

        self.ingredient_recipe_1 = IngredientInRecipe.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient_1,
            amount=5
        )
        self.ingredient_recipe_2 = IngredientInRecipe.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient_2,
            amount=200
        )

        self.url = reverse('api:recipes-list')

    def check_object(self, data, obj):
        self.assertEqual(data.get('id'), obj.pk)
        self.assertEqual(data.get('name'), obj.name)

    def test_get_list(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.check_object(resp.data[0], self.recipe)
