# coding: utf-8

from django.test import TestCase

from users.tests.factories import UserFactory
import factories
from ..templatetags.products_tags import can_like


class TemplateTagsTestCase(TestCase):
    def setUp(self):
        self.product = factories.ProductFactory()
        self.user = UserFactory()

    def test_can_like(self):
        """
        Check can user make like
        """

        self.assertFalse(can_like(self.product.likes, None))
        self.assertTrue(can_like(self.product.likes, self.user.id))

        factories.LikeFactory(product=self.product, user=self.user)

        self.assertFalse(can_like(self.product.likes, self.user.id))




