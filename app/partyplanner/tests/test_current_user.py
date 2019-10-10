from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


def make_token(user):
    """Creates a valid jwt for the given user"""
    from rest_framework_jwt.settings import api_settings

    payload = api_settings.JWT_PAYLOAD_HANDLER(user)
    token = api_settings.JWT_ENCODE_HANDLER(payload)
    return token


class TestCurrentUser(TestCase):
    fixtures = ['users.json']

    def test_valid_token(self):
        """Should return 200 with the user data"""
        user = User.objects.get(pk=70001)  # test user
        token = make_token(user)
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        resp = self.client.get('/whoami/', **headers)

        assert resp.status_code == 200

        blob = resp.json()
        assert blob == {
            'username': 'test_user',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_no_token(self):
        """Should return 401"""
        pass

    def test_expired_token(self):
        """Should return 401"""
        pass
