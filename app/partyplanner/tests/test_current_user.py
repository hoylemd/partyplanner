from django.contrib.auth import get_user_model

from .utils import JSONTestCase, make_token

User = get_user_model()


class TestCurrentUser(JSONTestCase):
    fixtures = ['users.json']

    def test_valid_token(self):
        """Should return 200 with the user data"""
        user = User.objects.get(pk=70001)  # test user
        token = make_token(user)
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        resp = self.client.get('/api/whoami/', **headers)

        self.assertContainsJSON(resp, {
            'username': 'test_user',
            'first_name': 'Test',
            'last_name': 'User'
        })

    def test_no_token(self):
        """Should return 401"""
        headers = {}
        resp = self.client.get('/api/whoami/', **headers)

        self.assertEqual(resp.status_code, 401)

    def test_expired_token(self):
        """Should return 401"""
        user = User.objects.get(pk=70001)  # test user
        token = make_token(user, expired=True)
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        resp = self.client.get('/api/whoami/', **headers)
        self.assertContainsJSON(
            resp, {'detail': 'Signature has expired.'}, status_code=401
        )
