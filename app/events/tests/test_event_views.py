from datetime import datetime
import json

from django.contrib.auth import get_user_model

from partyplanner.tests.utils import JSONTestCase, make_token
from events.serializers import ISO_8601_FORMAT

User = get_user_model()


class TestRetrieveEvent(JSONTestCase):
    fixtures = ['users.json', 'events.json']

    def test_get_event(self):
        """Should return 200 with the event data"""
        user = User.objects.get(pk=70001)  # test user
        token = make_token(user)
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        resp = self.client.get('/api/events/80001/', **headers)

        self.assertContainsJSON(resp, {
            'pk': 80001,
            'name': 'Test Event',
            'image': 'http://example.com/event-image.png',
            'starts_at': '2019-10-15T08:00:00Z'  # != fixture? normalized!
        })

    def test_get_event__notfound(self):
        """Should return 404"""
        user = User.objects.get(pk=70001)  # test user
        token = make_token(user)
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        resp = self.client.get('/api/events/80501/', **headers)

        self.assertContainsJSON(
            resp, {'detail': 'Not found.'}, status_code=404
        )

    def test_get_event__unauth(self):
        """Should return 401"""
        headers = {}
        resp = self.client.get('/api/events/80001/', **headers)

        self.assertContainsJSON(
            resp,
            {'detail': 'Authentication credentials were not provided.'},
            status_code=401
        ),


class TestCreateEvent(JSONTestCase):
    fixtures = ['users.json', 'events.json']

    def test_create_event(self):
        """Should return 201 with event data"""
        user = User.objects.get(pk=70001)  # test user
        token = make_token(user)
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        payload = {
            'name': 'New Years Bonanza!',
            'starts_at': datetime(year=2019, month=12, day=31, hour=22),
            'ends_at': datetime(year=2020, month=1, day=1, hour=2)
        }

        resp = self.client.post('/api/events/', payload, **headers)

        self.assertContainsJSON(
            resp,
            {
                'name': 'New Years Bonanza!',
                'description': '',
                'owner_id': 70001,
                'ends_at': '2020-01-01T02:00:00Z'
            },
            status_code=201
        )

    def test_create_event__missing_fields(self):
        """Should return 400 with field errors"""
        user = User.objects.get(pk=70001)  # test user
        token = make_token(user)
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        payload = {'name': 'TIMELESS PARTY'}

        resp = self.client.post('/api/events/', payload, **headers)

        self.assertContainsJSON(
            resp,
            {
                'starts_at': ['This field is required.'],
                'ends_at': ['This field is required.'],
            },
            status_code=400
        )

    def test_create_event__no_start_time(self):
        """Should return 400 with field errors

        Added to test an edge case with end_data validation
        """
        user = User.objects.get(pk=70001)  # test user
        token = make_token(user)
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        payload = {
            'name': 'ETERNAL PARTY',
            'ends_at': datetime(year=2020, month=1, day=1, hour=2)
        }

        resp = self.client.post('/api/events/', payload, **headers)

        self.assertContainsJSON(
            resp,
            {
                'starts_at': ['This field is required.'],
            },
            status_code=400
        )

    def test_create_event__unauth(self):
        """Should return 401"""
        headers = {}

        payload = {
            'name': 'New Years Bonanza!',
            'starts_at': datetime(year=2019, month=12, day=31, hour=22),
            'ends_at': datetime(year=2020, month=1, day=1, hour=2)
        }

        resp = self.client.post('/api/events/', payload, **headers)

        self.assertContainsJSON(
            resp,
            {'detail': 'Authentication credentials were not provided.'},
            status_code=401
        )

    def test_create_event__try_set_pk(self):
        """Should return 201, but not take the provided pk"""
        user = User.objects.get(pk=70001)  # test user
        token = make_token(user)
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        payload = {
            'pk': 80032,
            'name': 'New Years Bonanza!',
            'starts_at': datetime(year=2019, month=12, day=31, hour=22),
            'ends_at': datetime(year=2020, month=1, day=1, hour=2)
        }

        resp = self.client.post('/api/events/', payload, **headers)

        self.assertContainsJSON(
            resp,
            {
                'pk': lambda x: x != 80032,  # check pk not set to spec'd val
                'owner_id': 70001,
            },
            status_code=201
        )

    def test_create_event__invalid_time(self):
        """Should return 400 with error details"""
        user = User.objects.get(pk=70001)  # test user
        token = make_token(user)
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        payload = {
            'name': 'New Years Bonanza!',
            'starts_at': datetime(year=2019, month=12, day=31, hour=22),
            'ends_at': datetime(year=2018, month=1, day=1, hour=2)  # 2 years b4
        }

        resp = self.client.post('/api/events/', payload, **headers)

        self.assertContainsJSON(
            resp,
            {
                'ends_at': ['End time before start time.']
            },
            status_code=400
        )


class TestEditEvent(JSONTestCase):
    fixtures = ['users.json', 'events.json']

    def test_edit_event(self):
        """Should return 200 with updated event info"""
        user = User.objects.get(pk=70001)  # test user
        token = make_token(user)
        headers = {
            'HTTP_AUTHORIZATION': f'JWT {token}',
            'CONTENT_TYPE': 'application/json',  # required for patch
        }

        new_end_time = datetime(year=2019, month=10, day=16, hour=1)
        payload = json.dumps({
            'name': 'TESTING WHEEE!!!!',
            'ends_at': datetime.strftime(new_end_time, ISO_8601_FORMAT)
        })

        resp = self.client.patch('/api/events/80001/', payload, **headers)

        self.assertContainsJSON(
            resp,
            {
                'name': 'TESTING WHEEE!!!!',
                'description': 'This is an event for testing purposes',
                'owner_id': 70001,
                'ends_at': '2019-10-16T01:00:00Z'
            },
            status_code=200
        )

    def test_edit_event__unauth(self):
        """Should return 401"""
        headers = {
            'CONTENT_TYPE': 'application/json',  # required for patch
        }

        new_end_time = datetime(year=2019, month=10, day=16, hour=1)
        payload = json.dumps({
            'name': 'TESTING WHEEE!!!!',
            'ends_at': datetime.strftime(new_end_time, ISO_8601_FORMAT)
        })

        resp = self.client.patch('/api/events/80001/', payload, **headers)

        self.assertContainsJSON(
            resp,
            {'detail': 'Authentication credentials were not provided.'},
            status_code=401
        )

    def test_edit_event__not_owner(self):
        """Should return 403"""
        user = User.objects.get(pk=70002)  # 2nd test user
        token = make_token(user)
        headers = {
            'HTTP_AUTHORIZATION': f'JWT {token}',
            'CONTENT_TYPE': 'application/json',  # required for patch
        }

        new_end_time = datetime(year=2019, month=10, day=16, hour=1)
        payload = json.dumps({
            'name': 'TESTING WHEEE!!!!',
            'ends_at': datetime.strftime(new_end_time, ISO_8601_FORMAT)
        })

        resp = self.client.patch('/api/events/80001/', payload, **headers)

        self.assertContainsJSON(
            resp,
            {'detail': 'You do not have permission to perform this action.'},
            status_code=403
        )

    def test_edit_event__invalid_time(self):
        """Should return 400 with error detail"""
        pass

    def test_full_replace(self):
        """Should return 200 with updated info"""
        pass

    def test_full_replace__missing_field(self):
        """Should return 400 with error detail"""
        pass
