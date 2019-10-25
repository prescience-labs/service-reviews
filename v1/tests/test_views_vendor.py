from uuid import uuid4

from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient

from common.models import Product, Vendor

BASE_URL = '/v1/vendors'
headers  = {
    'HTTP_Authorization': 'Basic ' + settings.AUTH_SERVICE['CLIENT_ID'] + ':' + settings.AUTH_SERVICE['CLIENT_SECRET'],
}

class VendorListViewTests(TestCase):
    def setUp(self):
        self.client     = APIClient()
        self.vendor     = Vendor.objects.create(name='Test Vendor')
        self.team_id    = uuid4()

    def test_no_vendors(self):
        """Ensures that an empty response (no data existing) looks as expected"""
        self.vendor.delete()
        request         = self.client.get(BASE_URL, **headers)
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
            'team_id': self.team_id,
            'integrations_type': test_vendor_integrations_type,
            'integrations_id': test_vendor_integrations_id,
        }, **headers)
        self.assertEqual(request.status_code, 201)
        self.assertEqual(test_vendor_name, request.data['name'])
        self.assertEqual(test_vendor_integrations_type, request.data['integrations_type'])
        self.assertEqual(test_vendor_integrations_id, request.data['integrations_id'])

    def test_post_vendor_no_name(self):
        """Should return a clean 400 error and helpful text"""
        test_vendor_integrations_type   = 'test_type'
        test_vendor_integrations_id     = str(uuid4())
        request = self.client.post(BASE_URL, {
            'team_id': self.team_id,
            'integrations_type': test_vendor_integrations_type,
            'integrations_id': test_vendor_integrations_id,
        }, **headers)
        self.assertContains(request, 'name', status_code=400)

    def test_post_vendor_no_team_id(self):
        """Should return a 201 and create the team for me"""
        test_vendor_name                = 'Test Vendor'
        test_vendor_integrations_type   = 'test_type'
        test_vendor_integrations_id     = str(uuid4())
        request = self.client.post(BASE_URL, {
            'name': test_vendor_name,
            'integrations_type': test_vendor_integrations_type,
            'integrations_id': test_vendor_integrations_id,
        }, **headers)
        self.assertContains(request, 'team_id', status_code=201)

    def test_post_vendor_no_integrations_type(self):
        """Should still create the object with a 201"""
        test_vendor_name                = 'Test Vendor'
        test_vendor_integrations_id     = str(uuid4())
        request = self.client.post(BASE_URL, {
            'name': test_vendor_name,
            'team_id': self.team_id,
            'integrations_id': test_vendor_integrations_id,
        }, **headers)
        self.assertEqual(request.status_code, 201)
        self.assertEqual(test_vendor_name, request.data['name'])
        self.assertEqual(test_vendor_integrations_id, request.data['integrations_id'])

    def test_post_vendor_no_integrations_id(self):
        """Should still create the object with a 201"""
        test_vendor_name                = 'Test Vendor'
        test_vendor_integrations_type   = 'test_type'
        request = self.client.post(BASE_URL, {
            'name': test_vendor_name,
            'team_id': self.team_id,
            'integrations_type': test_vendor_integrations_type,
        }, **headers)
        self.assertEqual(request.status_code, 201)
        self.assertEqual(test_vendor_name, request.data['name'])
        self.assertEqual(test_vendor_integrations_type, request.data['integrations_type'])

    def test_post_vendor_products_with_all_data(self):
        """Should return a 201"""
        product_name        = 'Test Product'
        vendor_product_id   = '3201'
        request = self.client.post(f'{BASE_URL}/{self.vendor.id}/products', {
            'name': product_name,
            'team_id': self.team_id,
            'vendor_product_id': vendor_product_id,
        }, **headers)
        self.assertContains(request, product_name, status_code=201)

    def test_post_vendor_products_without_name(self):
        """Should return a 400 and contain helpful information"""
        request = self.client.post(f'{BASE_URL}/{self.vendor.id}/products', {
            'team_id': self.team_id,
            'vendor_product_id': '3201',
        }, **headers)
        self.assertContains(request, 'name', status_code=400)

    def test_post_vendor_products_without_team_id(self):
        """Should return a 201 and use the vendor's team id"""
        request = self.client.post(f'{BASE_URL}/{self.vendor.id}/products', {
            'name': 'Test vendor',
            'vendor_product_id': '3201',
        }, **headers)
        print(request.json())
        self.assertContains(request, 'team_id', status_code=201)
        self.assertEqual(request.json()['team_id'], self.vendor.team_id)

    def test_post_vendor_products_without_vendor_product_id(self):
        """Should return a 400 and contain helpful information"""
        request = self.client.post(f'{BASE_URL}/{self.vendor.id}/products', {
            'name': 'Test Product',
            'team_id': self.team_id,
        }, **headers)
        self.assertContains(request, 'vendor_product_id', status_code=400)
