from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsAuthenticatedUser
from api.serializers.favorite import FavoriteSerializer
from recipes.models import Favorite, Recipe


class FavoriteViewSet(viewsets.ModelViewSet):
    """Вьюсет для добавления/удаления рецепта в/из избранное(ого)."""

    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticatedUser,)

    @action(methods=['delete'], detail=False)
    def delete(self, request, *args, **kwargs):
        """Метод для удаления рецепта из избранного. """
        user = self.request.user
        recipe = Recipe.objects.get(pk=int(kwargs['id']))
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            Favorite.objects.get(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            data={'detail': 'Рецепт не добавлен в избранное!'},
            status=status.HTTP_400_BAD_REQUEST
        )
