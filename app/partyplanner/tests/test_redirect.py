from django.test import TestCase


class TestRedirect(TestCase):
    def test_redirect(self):
        """Should recirect to '/app'"""
        resp = self.client.get('/')

        # fetch_redirect_response is false because /app is not part of this
        # django application (it's the SPA)
        self.assertRedirects(resp, '/app', fetch_redirect_response=False)
