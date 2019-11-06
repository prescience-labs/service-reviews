from uuid import uuid4

from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient
import requests

from common.models import Product, Vendor
from ._helpers import get_client_auth_header, get_user_auth_header

BASE_URL = '/v1/vendors'

class VendorListViewClientAuthTest(TestCase):
    def setUp(self):
        self.client     = APIClient()
        self.vendor     = Vendor.objects.create(name='Test Vendor')
        self.team_id    = settings.TESTING['team_id']

        self.client_auth_headers    = {'HTTP_Authorization':get_client_auth_header()}
        self.user_auth_headers      = {'HTTP_Authorization':get_user_auth_header()}

    def test_no_vendors(self):
        """Ensures that an empty response (no data existing) looks as expected"""
        self.vendor.delete()
        expected_result = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': [],
        }

        # client auth
        client_request = self.client.get(BASE_URL, **self.client_auth_headers)
        self.assertDictEqual(client_request.data, expected_result)

        # user auth
        user_request = self.client.get(BASE_URL, **self.user_auth_headers)
        self.assertDictEqual(user_request.data, expected_result)

    def test_post_vendor(self):
        """Should add a vendor and return vendor data"""
        # client auth
        test_vendor_name                = 'Test Vendor 1'
        test_vendor_integrations_type   = 'test_type'
        test_vendor_integrations_id     = str(uuid4())
        client_request = self.client.post(BASE_URL, {
            'name': test_vendor_name,
            'team_id': self.team_id,
            'integrations_type': test_vendor_integrations_type,
            'integrations_id': test_vendor_integrations_id,
        }, **self.client_auth_headers)
        self.assertEqual(client_request.status_code, 201)
        self.assertEqual(test_vendor_name, client_request.data['name'])
        self.assertEqual(test_vendor_integrations_type, client_request.data['integrations_type'])
        self.assertEqual(test_vendor_integrations_id, client_request.data['integrations_id'])

        # user auth
        test_vendor_name                = 'Test Vendor 2'
        test_vendor_integrations_type   = 'test_type'
        test_vendor_integrations_id     = str(uuid4())
        user_request = self.client.post(BASE_URL, {
            'name': test_vendor_name,
            'team_id': self.team_id,
            'integrations_type': test_vendor_integrations_type,
            'integrations_id': test_vendor_integrations_id,
        }, **self.user_auth_headers)
        self.assertEqual(user_request.status_code, 201)
        self.assertEqual(test_vendor_name, user_request.data['name'])
        self.assertEqual(test_vendor_integrations_type, user_request.data['integrations_type'])
        self.assertEqual(test_vendor_integrations_id, user_request.data['integrations_id'])

    def test_post_vendor_no_name(self):
        """Should return a clean 400 error and helpful text"""
        # client auth
        test_vendor_integrations_type   = 'test_type'
        test_vendor_integrations_id     = str(uuid4())
        client_request = self.client.post(BASE_URL, {
            'team_id': self.team_id,
            'integrations_type': test_vendor_integrations_type,
            'integrations_id': test_vendor_integrations_id,
        }, **self.client_auth_headers)
        self.assertContains(client_request, 'name', status_code=400)

        # user auth
        test_vendor_integrations_type   = 'test_type'
        test_vendor_integrations_id     = str(uuid4())
        user_request = self.client.post(BASE_URL, {
            'team_id': self.team_id,
            'integrations_type': test_vendor_integrations_type,
            'integrations_id': test_vendor_integrations_id,
        }, **self.user_auth_headers)
        self.assertContains(user_request, 'name', status_code=400)

    def test_post_vendor_no_team_id(self):
        """Should return a 201 and create the team for me"""
        # client auth
        test_vendor_name                = 'Test Vendor'
        test_vendor_integrations_type   = 'test_type'
        test_vendor_integrations_id     = str(uuid4())
        client_request = self.client.post(BASE_URL, {
            'name': test_vendor_name,
            'integrations_type': test_vendor_integrations_type,
            'integrations_id': test_vendor_integrations_id,
        }, **self.client_auth_headers)
        self.assertContains(client_request, 'team_id', status_code=201)

        # user auth
        test_vendor_name                = 'Test Vendor'
        test_vendor_integrations_type   = 'test_type'
        test_vendor_integrations_id     = str(uuid4())
        user_request = self.client.post(BASE_URL, {
            'name': test_vendor_name,
            'integrations_type': test_vendor_integrations_type,
            'integrations_id': test_vendor_integrations_id,
        }, **self.user_auth_headers)
        self.assertContains(user_request, 'team_id', status_code=201)

    def test_post_vendor_no_integrations_type(self):
        """Should still create the object with a 201"""
        # client auth
        test_vendor_name                = 'Test Vendor'
        test_vendor_integrations_id     = str(uuid4())
        client_request = self.client.post(BASE_URL, {
            'name': test_vendor_name,
            'team_id': self.team_id,
            'integrations_id': test_vendor_integrations_id,
        }, **self.client_auth_headers)
        self.assertEqual(client_request.status_code, 201)
        self.assertEqual(test_vendor_name, client_request.data['name'])
        self.assertEqual(test_vendor_integrations_id, client_request.data['integrations_id'])

        # user auth
        test_vendor_name                = 'Test Vendor'
        test_vendor_integrations_id     = str(uuid4())
        user_request = self.client.post(BASE_URL, {
            'name': test_vendor_name,
            'team_id': self.team_id,
            'integrations_id': test_vendor_integrations_id,
        }, **self.user_auth_headers)
        self.assertEqual(user_request.status_code, 201)
        self.assertEqual(test_vendor_name, user_request.data['name'])
        self.assertEqual(test_vendor_integrations_id, user_request.data['integrations_id'])

    def test_post_vendor_no_integrations_id(self):
        """Should still create the object with a 201"""
        # client auth
        test_vendor_name                = 'Test Vendor'
        test_vendor_integrations_type   = 'test_type'
        client_auth = self.client.post(BASE_URL, {
            'name': test_vendor_name,
            'team_id': self.team_id,
            'integrations_type': test_vendor_integrations_type,
        }, **self.client_auth_headers)
        self.assertEqual(client_auth.status_code, 201)
        self.assertEqual(test_vendor_name, client_auth.data['name'])
        self.assertEqual(test_vendor_integrations_type, client_auth.data['integrations_type'])

        # user auth
        test_vendor_name                = 'Test Vendor'
        test_vendor_integrations_type   = 'test_type'
        user_auth = self.client.post(BASE_URL, {
            'name': test_vendor_name,
            'team_id': self.team_id,
            'integrations_type': test_vendor_integrations_type,
        }, **self.user_auth_headers)
        self.assertEqual(user_auth.status_code, 201)
        self.assertEqual(test_vendor_name, user_auth.data['name'])
        self.assertEqual(test_vendor_integrations_type, user_auth.data['integrations_type'])

    def test_post_vendor_products_with_all_data(self):
        """Should return a 201"""
        # client auth
        product_name        = 'Test Product'
        vendor_product_id   = str(uuid4())
        client_request = self.client.post(f'{BASE_URL}/{self.vendor.id}/products', {
            'name': product_name,
            'team_id': self.team_id,
            'vendor_product_id': vendor_product_id,
        }, **self.client_auth_headers)
        self.assertContains(client_request, product_name, status_code=201)

        # user auth
        product_name        = 'Test Product'
        vendor_product_id   = str(uuid4())
        user_request = self.client.post(f'{BASE_URL}/{self.vendor.id}/products', {
            'name': product_name,
            'team_id': self.team_id,
            'vendor_product_id': vendor_product_id,
        }, **self.user_auth_headers)
        self.assertContains(user_request, product_name, status_code=201)

    def test_post_vendor_products_without_name(self):
        """Should return a 400 and contain helpful information"""
        # client_auth
        client_request = self.client.post(f'{BASE_URL}/{self.vendor.id}/products', {
            'team_id': self.team_id,
            'vendor_product_id': str(uuid4()),
        }, **self.client_auth_headers)
        self.assertContains(client_request, 'name', status_code=400)

        # user auth
        user_request = self.client.post(f'{BASE_URL}/{self.vendor.id}/products', {
            'team_id': self.team_id,
            'vendor_product_id': str(uuid4()),
        }, **self.user_auth_headers)
        self.assertContains(user_request, 'name', status_code=400)

    def test_post_vendor_products_without_team_id(self):
        """Should return a 201 and use the vendor's team id"""
        # client request
        client_request = self.client.post(f'{BASE_URL}/{self.vendor.id}/products', {
            'name': 'Test vendor',
            'vendor_product_id': str(uuid4()),
        }, **self.client_auth_headers)
        self.assertContains(client_request, 'team_id', status_code=201)
        self.assertEqual(client_request.json()['team_id'], self.vendor.team_id)

        # user request
        user_request = self.client.post(f'{BASE_URL}/{self.vendor.id}/products', {
            'name': 'Test vendor',
            'vendor_product_id': str(uuid4()),
        }, **self.user_auth_headers)
        self.assertContains(user_request, 'team_id', status_code=201)
        self.assertEqual(user_request.json()['team_id'], self.vendor.team_id)

    def test_post_vendor_products_without_vendor_product_id(self):
        """Should return a 400 and contain helpful information"""
        # client request
        client_request = self.client.post(f'{BASE_URL}/{self.vendor.id}/products', {
            'name': 'Test Product',
            'team_id': self.team_id,
        }, **self.client_auth_headers)
        self.assertContains(client_request, 'vendor_product_id', status_code=400)

        # user request
        user_request = self.client.post(f'{BASE_URL}/{self.vendor.id}/products', {
            'name': 'Test Product',
            'team_id': self.team_id,
        }, **self.user_auth_headers)
        self.assertContains(user_request, 'vendor_product_id', status_code=400)
