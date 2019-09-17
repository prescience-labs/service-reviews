from uuid import uuid4

from django.test import TestCase
from rest_framework.test import APIClient

BASE_URL = '/v1/vendors'

class VendorListViewTests(TestCase):
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

    def test_post_vendor(self):
        """Should add a vendor and return vendor data"""
        test_vendor_name                = 'Test Vendor 1'
        test_vendor_integrations_type   = 'test_type'
        test_vendor_integrations_id     = str(uuid4())
        request = self.client.post(BASE_URL, {
            'name': test_vendor_name,
            'integrations_type': test_vendor_integrations_type,
            'integrations_id': test_vendor_integrations_id,
        })
        self.assertEqual(request.status_code, 201)
        self.assertTrue('id' in request.data)
        self.assertEqual(test_vendor_name, request.data['name'])
        self.assertEqual(test_vendor_integrations_type, request.data['integrations_type'])
        self.assertEqual(test_vendor_integrations_id, request.data['integrations_id'])
        self.assertTrue('created_at' in request.data)
        self.assertTrue('updated_at' in request.data)

    def test_post_vendor_no_name(self):
        """Should return a clean 400 error"""
        test_vendor_name                = ''
        test_vendor_integrations_type   = 'test_type'
        test_vendor_integrations_id     = str(uuid4())
        request = self.client.post(BASE_URL, {
            'name': test_vendor_name,
            'integrations_type': test_vendor_integrations_type,
            'integrations_id': test_vendor_integrations_id,
        })
        self.assertEqual(request.status_code, 400)

    def test_post_vendor_no_integrations_type(self):
        """Should still create the object with a 201"""
        test_vendor_name                = 'Test Vendor'
        test_vendor_integrations_type   = ''
        test_vendor_integrations_id     = str(uuid4())
        request = self.client.post(BASE_URL, {
            'name': test_vendor_name,
            'integrations_type': test_vendor_integrations_type,
            'integrations_id': test_vendor_integrations_id,
        })
        self.assertEqual(request.status_code, 201)
        self.assertTrue('id' in request.data)
        self.assertEqual(test_vendor_name, request.data['name'])
        self.assertEqual(test_vendor_integrations_type, request.data['integrations_type'])
        self.assertEqual(test_vendor_integrations_id, request.data['integrations_id'])
        self.assertTrue('created_at' in request.data)
        self.assertTrue('updated_at' in request.data)

    def test_post_vendor_no_integrations_id(self):
        """Should still create the object with a 201"""
        test_vendor_name                = 'Test Vendor'
        test_vendor_integrations_type   = 'test_type'
        test_vendor_integrations_id     = ''
        request = self.client.post(BASE_URL, {
            'name': test_vendor_name,
            'integrations_type': test_vendor_integrations_type,
            'integrations_id': test_vendor_integrations_id,
        })
        self.assertEqual(request.status_code, 201)
        self.assertTrue('id' in request.data)
        self.assertEqual(test_vendor_name, request.data['name'])
        self.assertEqual(test_vendor_integrations_type, request.data['integrations_type'])
        self.assertEqual(test_vendor_integrations_id, request.data['integrations_id'])
        self.assertTrue('created_at' in request.data)
        self.assertTrue('updated_at' in request.data)
