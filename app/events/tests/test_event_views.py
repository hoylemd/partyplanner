from partyplanner.tests.utils import JSONTestCase


class TestEventViews(JSONTestCase):
    fixtures = ['events.json']

    def test_get_event(self):
        """Should return 200 with the event data"""
        pass

    def test_get_event__notfound(self):
        """Should return 404"""
        pass

    def test_get_event__unauth(self):
        """Should return 401"""
        pass
