from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

ERROR_MESSAGE = 'У вас недостаточно прав для выполнения данного действия.'


class IsAuthenticatedUser(permissions.BasePermission):
    """Permission класс для аутентифицированных пользователей."""
    def has_permission(self, request, view):
        return request.user.is_authenticated


class AuthorOrReadonly(permissions.BasePermission):
    """Permission класс для аутентифицированных пользователей для safe методов и возможностью редактирования
    и удаления только своего контента."""
    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if obj.author != request.user:
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                raise PermissionDenied(ERROR_MESSAGE)
        return True
