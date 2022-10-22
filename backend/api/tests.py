from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from recipes.ingredients.models import Ingredient


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
