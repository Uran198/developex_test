from django.contrib.auth.hashers import make_password

import factory

from .models import CardUser


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CardUser

    number = factory.Sequence(lambda n: str(n).rjust(16, '0'))
    balance = 1000
    is_blocked = False
    password = make_password('1234')
