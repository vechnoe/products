# coding: utf-8

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from users.tests.factories import UserFactory
import factories
from ..models import Like
from ..forms import CommentForm


class ViewsTest(TestCase):
    """
    Test product's views
    """

    def setUp(self):
        self.user = UserFactory()

    def _log_in_and_test(self, user):
        if user is not None:
            logged_in = self.client.login(
                username=user.username, password='test')
            self.assertTrue(logged_in)

    def _test_product_detail(self, product):
        response = self.client.get(
            reverse('products:product_detail',
                    kwargs={'slug': product.slug}))

        self.assertEqual(response.status_code, 200)
        return response.context

    def test_user_post_to_send_like(self):
        """
        Test user like and send post request
        """
        product = factories.ProductFactory()

        self._log_in_and_test(self.user)
        self.assertEqual(Like.objects.all().count(), 0)

        response = self.client.post(
            reverse('products:like_create'),
            {'productId': product.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            response.content, {'message': 'Thanks for your feedback'})
        self.assertEqual(Like.objects.all().count(), 1)

    def test_products_list_view(self):
        """
        Test product's list view
        """
        factories.ProductFactory.create_batch(20)
        response = self.client.get(reverse('products:products_list'))
        object_list = response.context['object_list']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(object_list.count(), 20)

    def test_product_detail_view(self):
        """
        Test product's an instance on product detail page
        """
        product = factories.ProductFactory()
        context_object = self._test_product_detail(product)['product']
        self.assertEqual(context_object.name, product.name)

    def test_product_detail_with_comments_list(self):
        """
        Test product's comments
        """
        product = factories.ProductFactory()
        now = timezone.now()
        yesterday = timezone.now() - timezone.timedelta(days=1)

        factories.CommentFactory.create_batch(
            2, created_at=yesterday, product=product)
        factories.CommentFactory.create_batch(
            5, created_at=now, product=product)

        context_object = self._test_product_detail(product)['product']
        self.assertEqual(context_object.comments.count(), 5)

    def test_product_detail_with_comment_form(self):
        """
        Checking comment's form
        """
        product = factories.ProductFactory()
        context = self._test_product_detail(product)
        self.assertIsInstance(context['form'], CommentForm)

    def test_invalid_comment_form(self):
        """
        Check required field
        """
        product = factories.ProductFactory()
        response = self.client.post(
            reverse('products:product_detail', kwargs={'slug': product.slug}),
            {'text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', 'text', 'This field is required.')

    def test_post_to_valid_comment_form(self):
        """
        Check post data when comment form is valid
        """
        product = factories.ProductFactory()
        self.assertEqual(product.comments.count(), 0)
        response = self.client.post(
            reverse('products:product_detail', kwargs={'slug': product.slug}),
            {'text': 'something'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(product.comments.count(), 1)






