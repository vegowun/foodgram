from django.apps import AppConfig

ADMIN = 'admin'
USER = 'user'

ROLES = [
    (ADMIN, 'Администратор'),
    (USER, 'Пользователь'),
]


class UsersConfig(AppConfig):
    name = 'users'
