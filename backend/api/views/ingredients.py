from rest_framework import viewsets

from api.serializers.ingredients import IngredientSerializer
from recipes.ingredients.models import Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет ингредиентов"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
