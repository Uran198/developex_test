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
    wrong_tries = models.IntegerField(default=0)

    objects = CardUserManager()

    USERNAME_FIELD = 'number'

    def get_absolute_url(self):
        return '/'

    def get_username(self):
        return self.number


OPERATION_CHOICES = (
    ('WD', 'Withdraw money'),
    ('CB', 'Check balance'),
)


class Transaction(models.Model):
    operation = models.CharField(max_length=2, choices=OPERATION_CHOICES)
    date = models.DateTimeField(auto_now=True)
    card = models.ForeignKey(CardUser)
    amount = models.PositiveIntegerField(blank=True, null=True)
