from django.contrib.auth import get_user_model

from partyplanner.tests.utils import JSONTestCase, make_token

User = get_user_model()


class TestEventViews(JSONTestCase):
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
            'starts_at': '2019-10-15T13:00:00Z'  # != fixture? normalized!
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
        )
