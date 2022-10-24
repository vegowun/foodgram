from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from users.apps import ADMIN


class CustomUserManager(BaseUserManager):
    """Кастомный user менеджер"""
    def create_superuser(self, username, email, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', ADMIN)
        return self.create_user(username, email, **extra_fields)
