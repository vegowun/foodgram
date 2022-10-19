from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    AUTH_USER_MODEL = 'users.User'
