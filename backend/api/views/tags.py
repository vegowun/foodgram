from rest_framework import viewsets

from api.serializers.tags import TagSerializer
from recipes.models import Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет тегов"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
