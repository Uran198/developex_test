from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CardUserManager(BaseUserManager):
    use_in_migrations = True


class CardUser(AbstractBaseUser):
    number = models.CharField(
        max_length=16,
        unique=True,
        validators=[
            validators.RegexValidator(
                '\d{16}',
                "Number must be of length 16 and must consist only of numbers"
                )
            ]
        )
    balance = models.IntegerField()
    is_blocked = models.BooleanField()
    objects = CardUserManager()

    USERNAME_FIELD = 'number'

    def get_absolute_url(self):
        return '/'

    def get_username(self):
        return self.number
