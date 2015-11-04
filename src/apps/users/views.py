# coding: utf-8

from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect
from django.views.generic import FormView, RedirectView
from django.contrib import messages

from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login as auth_login, logout)

from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/products/'
    form_class = AuthenticationForm
    template_name = 'users/login_form.html'
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.success_url)
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        messages.add_message(
            self.request, messages.SUCCESS, 'You have successfully logged in')

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.REQUEST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self):
        logout(self.request)
        messages.add_message(
            self.request, messages.SUCCESS, 'You have successfully signed out')
        return reverse('products:products_list')
