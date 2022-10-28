from rest_framework import viewsets

from api.pagination import LimitPageNumberPagination
from api.permissions import AuthorOrReadonly
from api.serializers.recipes import RecipeSerializer, RecipeCreateEditSerializer
from recipes.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов класса Recipe"""

    queryset = Recipe.objects.all()
    pagination_class = LimitPageNumberPagination
    permission_classes = (AuthorOrReadonly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateEditSerializer
