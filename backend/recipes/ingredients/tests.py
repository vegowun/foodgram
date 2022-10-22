from backend.foodgram.wsgi import *

from unittest import TestCase

from recipes.ingredients.models import Ingredient


class IngredientModelTestCase(TestCase):
    def setUp(self) -> None:
        self.ingredient = Ingredient.objects.create()

    def tearDown(self) -> None:
        self.ingredient.delete()

    def test_name(self):
        self.assertEqual(str(self.ingredient), self.ingredient.name)
