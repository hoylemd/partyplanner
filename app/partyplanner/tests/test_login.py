from django.test import TestCase


class TestLogin(TestCase):
    fixtures = ['users.json']

    def test_login(self):
        """Should return 200 with auth token"""
        payload = {
            'username': 'test_user',
            'password': 'password123'
        }
        resp = self.client.post('/api/token-auth/', data=payload)
        assert resp.status_code == 200

        blob = resp.json()
        assert blob['token'] is not None

    def test_wrong_password(self):
        """Should return 401"""

        payload = {
            'username': 'test_user',
            'password': 'hunter2'
        }
        resp = self.client.post('/api/token-auth/', data=payload)
        assert resp.status_code == 400

        blob = resp.json()
        assert blob == {
            'non_field_errors': ['Unable to log in with provided credentials.']
        }
