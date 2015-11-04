# coding: utf-8

from django.utils import timezone

import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from users.tests.factories import UserFactory
from ..models import Product, Comment, Like


class ProductFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText()
    description = fuzzy.FuzzyText()
    price = fuzzy.FuzzyDecimal(0.00, precision=2)

    class Meta:
        model = Product


class CommentFactory(DjangoModelFactory):
    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(UserFactory)
    created_at = fuzzy.FuzzyDateTime(
        timezone.now() - timezone.timedelta(days=10), timezone.now())
    text = fuzzy.FuzzyText()

    class Meta:
        model = Comment


class LikeFactory(DjangoModelFactory):
    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Like
