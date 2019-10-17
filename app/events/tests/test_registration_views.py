from django.contrib.auth import get_user_model

from partyplanner.tests.utils import JSONTestCase, make_token, SpecHelpers

User = get_user_model()


class TestRegister(JSONTestCase):
    fixtures = ['users.json', 'events.json', 'attendance.json']

    def test_register(self):
        """Should return 201 (Created)"""
        user = User.objects.get(pk=70001)  # test user
        token = make_token(user)
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        resp = self.client.post('/api/events/80001/register', **headers)

        self.assertContainsJSON(resp, {
            'created_at': SpecHelpers.is_datetime,
            'event': 80001,
            'user': 70001
        }, status_code=201)

    def test_register__dupe(self):
        """Should return 400 (duplicate)"""
        user = User.objects.get(pk=70002)  # 2nd user
        token = make_token(user)
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        resp = self.client.post('/api/events/80001/register', **headers)

        self.assertContainsJSON(resp, {
            'detail': 'You are already registered for this event.'
        }, status_code=400)

    def test_register__unauth(self):
        """Should return 401"""
        headers = {}

        resp = self.client.post('/api/events/80001/register', **headers)

        self.assertContainsJSON(resp, {
            'detail': 'Authentication credentials were not provided.'
        }, status_code=401)

    def test_register__invalid_event(self):
        """Should return 404 (Event record not found)"""
        user = User.objects.get(pk=70001)  # test user
        token = make_token(user)
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        resp = self.client.post('/api/events/80009/register', **headers)

        self.assertContainsJSON(resp, {
            'detail': 'Event not found.'
        }, status_code=404)

    def test_unregister(self):
        """Should return 204 (No Content ~= deleted)"""
        user = User.objects.get(pk=70002)  # 2nd user
        token = make_token(user)
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        resp = self.client.delete('/api/events/80001/register', **headers)

        self.assertContainsJSON(resp, {}, status_code=204)

    def test_unregister__not_registered(self):
        """Should return 404 (Attendance record not found)"""
        pass

    def test_unregister__unauth(self):
        """Should return 401"""
        pass

    def test_unregister__invalid_event(self):
        """Should return 404 (Event record not found)"""
        pass
