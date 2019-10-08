from django.test import TestCase


class TestSignup(TestCase):
    def test_valid(self):
        """Should return 201 with the user data"""
        pass

    def test_no_email(self):
        """Should return 400 with error details"""
        pass
