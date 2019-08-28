"""
Modified from:
https://coderwall.com/p/sll1kw/django-auth-class-based-views-login-and-logout
"""

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic import FormView, RedirectView
from django.urls import reverse_lazy

from partyplanner.forms import SignUpForm


class Login(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = reverse_lazy('event_list')
    form_class = AuthenticationForm
    template_name = 'login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())

        return super().form_valid(form)


class Logout(RedirectView):
    """
    Provides users the ability to logout
    """
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class Signup(FormView):
    """
    Allows a user to sign up for an account
    """
    success_url = reverse_lazy('event_list')
    form_class = SignUpForm
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return super().form_valid(form)
