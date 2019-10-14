from django.contrib.auth import get_user_model, models as auth_models
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from events.permissions import ObjectOwnership
from events.models import Event

factory = APIRequestFactory()
User = get_user_model()


class DummyObjectView:
    """
    View mock class that just supplies 'get_object' with the passed object.
    """
    def __init__(self, obj):
        self.object = obj

    def get_object(self):
        return self.object


class TestObjectOwnership(TestCase):
    fixtures = ['users', 'events']

    def test_read_request(self):
        """Should permit"""
        request = factory.get('/1/')
        request.user = User.objects.get(pk=70001)  # test user

        assert ObjectOwnership().has_permission(request, None)

    def test_read_request__unauth(self):
        """Should refuse"""
        request = factory.get('/1/')
        request.user = auth_models.AnonymousUser()

        self.assertFalse(ObjectOwnership().has_permission(request, None))

    def test_create_request(self):
        """Should permit"""
        request = factory.post('/')
        request.user = User.objects.get(pk=70001)  # test user

        assert ObjectOwnership().has_permission(request, None)

    def test_create_request__unauth(self):
        """Should refuse"""
        request = factory.post('/')
        request.user = auth_models.AnonymousUser()

        self.assertFalse(ObjectOwnership().has_permission(request, None))

    def test_edit_request(self):
        """Should permit"""
        request = factory.patch('/80001')
        request.user = User.objects.get(pk=70001)  # test user
        view = DummyObjectView(Event.objects.get(pk=80001))

        assert ObjectOwnership().has_permission(request, view)

    def test_edit_request__unauth(self):
        """Should refuse"""
        request = factory.patch('/80001')
        request.user = auth_models.AnonymousUser()
        view = DummyObjectView(Event.objects.get(pk=80001))

        self.assertFalse(ObjectOwnership().has_permission(request, view))

    def test_edit_request__not_owner(self):
        """Should refuse"""
        request = factory.patch('/80001')
        request.user = User.objects.get(pk=70002)  # not owner of test event
        view = DummyObjectView(Event.objects.get(pk=80001))

        self.assertFalse(ObjectOwnership().has_permission(request, view))
