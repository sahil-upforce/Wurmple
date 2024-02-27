from django.contrib.auth.models import UserManager

from core.managers import BaseModelManager


class CustomUserManager(UserManager, BaseModelManager):
    pass
