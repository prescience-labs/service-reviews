from django.test import TestCase
from rest_framework.test import APIClient

BASE_URL = '/v1/vendors'

class VendorViewTests(TestCase):
    def __init__(self, *args, **kwargs):
        self.client = APIClient()
        super().__init__(*args, **kwargs)

    def test_no_vendors(self):
        """Ensures that an empty response (no data existing) looks as expected"""
        request         = self.client.get(BASE_URL)
        expected_result = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': [],
        }
        self.assertDictEqual(request.data, expected_result)
