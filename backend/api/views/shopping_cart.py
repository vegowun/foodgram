from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsAuthenticatedUser
from api.serializers.shopping_cart import ShoppingCartSerializer
from recipes.models import Recipe, ShoppingCart


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """Вьюсет для списка покупок."""

    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticatedUser,)

    @action(methods=['delete'], detail=False)
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        recipe = Recipe.objects.get(pk=int(kwargs['id']))
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            ShoppingCart.objects.get(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            data={'detail': 'Рецепт не добавлен в избранное!'},
            status=status.HTTP_400_BAD_REQUEST
        )
