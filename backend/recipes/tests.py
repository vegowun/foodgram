from unittest import TestCase

from recipes.models import Tag


class TagModelTestCase(TestCase):
    def setUp(self) -> None:
        self.tag = Tag.objects.create()

    def tearDown(self) -> None:
        self.tag.delete()

    def test_name(self):
        self.assertEqual(str(self.tag), self.tag.name)


class RecipeModelTestCase(TestCase):
    def setUp(self) -> None:
        self.recipe = Tag.objects.create()

    def tearDown(self) -> None:
        self.recipe.delete()

    def test_name(self):
        self.assertEqual(str(self.recipe), self.recipe.name)
