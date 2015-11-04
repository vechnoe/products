# coding: utf-8

from django.contrib.auth.models import User

import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

USER_PASSWORD = 'test'


class UserFactory(DjangoModelFactory):
    username = fuzzy.FuzzyText()
    password = factory.PostGenerationMethodCall('set_password', USER_PASSWORD)
    is_active = True

    class Meta:
        model = User


