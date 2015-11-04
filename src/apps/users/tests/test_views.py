from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

import factories


class ViewsTest(TestCase):
    """
    Test auth views
    """

    def setUp(self):
        self.user = factories.UserFactory()

    def tearDown(self):
        self.client.logout()
        User.objects.all().delete()

    def _log_in_and_test(self, user):
        if user is not None:
            logged_in = self.client.login(
                username=user.username, password=factories.USER_PASSWORD)
            self.assertTrue(logged_in)

    def test_login_form(self):
        """
        Checking login form
        """
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_invalid_login_form(self):
        """
        Check required field
        """
        response = self.client.post(
            reverse('users:login'), {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', 'username', 'This field is required.')
        self.assertFormError(
            response, 'form', 'password', 'This field is required.')

    def test_post_to_valid_login_form(self):
        """
        Check post valid data to login form
        """
        response = self.client.post(
            reverse('users:login'),
            {'username': self.user.username,
             'password': factories.USER_PASSWORD}
        )
        self.assertRedirects(response, reverse('products:products_list'))

    def test_login_form_when_user_logged_in(self):
        """
        Check redirect to /products/ when user is logged in
        """
        self._log_in_and_test(self.user)
        response = self.client.get(reverse('users:login'))
        self.assertRedirects(response, reverse('products:products_list'))
        self.assertEqual(
            int(self.client.session['_auth_user_id']), self.user.pk)

    def test_logout(self):
        """
        Check redirect to /products/ when logout
        """
        self._log_in_and_test(self.user)
        self.assertIsNotNone(self.client.session.get('_auth_user_id', None))

        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, reverse('products:products_list'))
        self.assertIsNone(self.client.session.get('_auth_user_id', None))










