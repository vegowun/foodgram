from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from api.serializers.ingredients import IngredientSerializer
from api.serializers.recipes import RecipeSerializer, RecipeCreateSerializer
from recipes.ingredients.models import Ingredient
from recipes.models import Recipe


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет рецептов класса Recipe"""

    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer

    @staticmethod
    def create_object(request, pk, serializers):
        pass
