from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api.filters import IngredientsFilter
from api.serializers.ingredients import IngredientSerializer
from recipes.ingredients.models import Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет ингредиентов"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter
    pagination_class = None
