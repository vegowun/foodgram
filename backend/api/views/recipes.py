from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api.filters import RecipesFilter
from api.pagination import LimitPageNumberPagination
from api.permissions import AuthorOrReadonly
from api.serializers.recipes import RecipeSerializer, RecipeCreateEditSerializer
from recipes.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов класса Recipe"""

    queryset = Recipe.objects.all()
    pagination_class = LimitPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipesFilter
    permission_classes = (AuthorOrReadonly,)

    def get_serializer_class(self):
        """Возврат необходимого сериализатора в зависимости от метода в запросе."""
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateEditSerializer
