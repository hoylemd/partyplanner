
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic import FormView, RedirectView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from partyplanner.forms import SignUpForm
from partyplanner.serializers import UserSerializer, UserSerializerWithToken


class Login(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = reverse_lazy('event_list')
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request)

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


class CurrentUser(APIView):
    """
    Determine the current user by their token, and return their data
    """
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
