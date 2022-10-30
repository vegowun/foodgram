from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.pagination import LimitPageNumberPagination
from api.permissions import IsAuthenticatedUser
from api.serializers.subscriptions import SubscribeSerializer
from recipes.models import Follow
from users.models import User


class SubscriptionsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для просмотра всех подписок."""

    serializer_class = SubscribeSerializer
    pagination_class = LimitPageNumberPagination
    permission_classes = (IsAuthenticatedUser,)

    def get_queryset(self):
        return self.request.user.follower.all()


class SubscribeViewSet(viewsets.ModelViewSet):
    """Вьюсет для подписки/отписки на/от пользователя."""

    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticatedUser,)

    @action(methods=['delete'], detail=False)
    def delete(self, request, *args, **kwargs):
        """Метод для отписки текущего пользователя от автора рецептов."""
        user = self.request.user
        author = User.objects.get(pk=int(kwargs['id']))
        if Follow.objects.filter(user=user, author=author).exists():
            Follow.objects.get(user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            data={'detail': 'Вы не подписаны на этого пользователя!'},
            status=status.HTTP_400_BAD_REQUEST
        )
