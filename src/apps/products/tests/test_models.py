# coding: utf-8

from decimal import Decimal

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from users.tests.factories import UserFactory
from ..models import Comment
import factories


class ProductTests(TestCase):

    def setUp(self):
        self.product = factories.ProductFactory()
        self.user = UserFactory()

    def test_product_generate_unique_slug(self):
        """
        Check unique slug is generated
        """
        product_one = factories.ProductFactory(name='Foo')
        product_two = factories.ProductFactory(name='Foo')
        self.assertNotEqual(product_one.slug, product_two.slug)

    def test_product_price(self):
        """
        Check price must be greater than negative
        """
        with self.assertRaises(ValidationError):
            factories.ProductFactory(price=Decimal('-0.01'))

    def test_latest_comments_manager(self):
        """
        Check manager returns only today comments
        """
        now = timezone.now()
        yesterday = timezone.now() - timezone.timedelta(days=1)

        factories.CommentFactory.create_batch(
            2, created_at=yesterday)
        factories.CommentFactory.create_batch(
            5, created_at=now, product=self.product)

        self.assertEqual(Comment.latest_comments.count(), 5)






