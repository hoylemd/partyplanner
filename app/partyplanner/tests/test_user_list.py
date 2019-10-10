from .utils import JSONTestCase, SpecHelpers


class TestUserList(JSONTestCase):
    def test_create_user(self):
        """Should return 201 with token"""
        payload = {
            'username': 'steve',
            'first_name': 'Steve',
            'last_name': 'Minecraft',
            'email': 'steve@example.com',
            'password': 'open_sesame'
        }

        resp = self.client.post('/users/', payload)

        self.assertContainsJSON(resp, {
            'token': SpecHelpers.is_jwt,
            'username': 'steve',
            'password': SpecHelpers.is_absent
        }, status_code=201)
