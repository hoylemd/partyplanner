from django.views.generic import RedirectView

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from partyplanner.serializers import UserSerializer, UserSerializerWithToken


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


class RedirectToApp(RedirectView):
    url = '/app'
