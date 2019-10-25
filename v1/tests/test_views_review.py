from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient

BASE_URL = '/v1/reviews'
headers  = {
    'HTTP_Authorization': 'Basic ' + settings.AUTH_SERVICE['CLIENT_ID'] + ':' + settings.AUTH_SERVICE['CLIENT_SECRET'],
}

class ReviewListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_no_reviews(self):
        """Ensures that an empty response (no data existing) looks as expected"""
        request         = self.client.get(BASE_URL, **headers)
        expected_result = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': [],
        }
        self.assertDictEqual(request.data, expected_result)
