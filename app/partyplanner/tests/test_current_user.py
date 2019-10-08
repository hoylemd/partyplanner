from django.test import TestCase


class TestCurrentUser(TestCase):
    fixtures = ['users.json']

    def test_valid_token(self):
        """Should return 200 with the user data"""
        pass

    def test_no_token(self):
        """Should return 401"""
        pass

    def test_expired_token(self):
        """Should return 401"""
        pass
