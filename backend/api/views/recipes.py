from rest_framework import viewsets

from api.pagination import LimitPageNumberPagination
from api.serializers.recipes import RecipeSerializer, RecipeCreateSerializer
from recipes.models import Recipe


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет рецептов класса Recipe"""

    queryset = Recipe.objects.all()
    pagination_class = LimitPageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer

    @staticmethod
    def create_object(request, pk, serializers):
        pass