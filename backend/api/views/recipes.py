from rest_framework import viewsets

from api.pagination import LimitPageNumberPagination
from api.permissions import IsAuthenticatedUser
from api.serializers.recipes import RecipeSerializer, RecipeCreateSerializer
from recipes.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов класса Recipe"""

    queryset = Recipe.objects.all()
    pagination_class = LimitPageNumberPagination
    permission_classes = (IsAuthenticatedUser,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer
