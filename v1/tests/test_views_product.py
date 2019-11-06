from uuid import uuid4

from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient

from common.models import Inventory, Product, Vendor
from ._helpers import get_client_auth_header, get_user_auth_header

BASE_URL = '/v1/products'

class ProductListViewTests(TestCase):
    def setUp(self):
        self.client     = APIClient()
        self.team_id    = settings.TESTING['team_id']
        self.product    = Product.objects.create(name='Test Product', team_id=self.team_id)

        self.client_auth_headers    = {'HTTP_Authorization':get_client_auth_header()}
        self.user_auth_headers      = {'HTTP_Authorization':get_user_auth_header()}

    def test_no_products(self):
        """Ensures that an empty response (no data existing) looks as expected"""
        self.product.delete()
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

    def test_post_product(self):
        """Should add a product and return product data"""
        test_product_name = 'Test Product 1'

        # client auth
        client_request = self.client.post(BASE_URL, {
            'name': test_product_name,
            'team_id': self.team_id,
        }, **self.client_auth_headers)
        self.assertTrue('id' in client_request.data)
        self.assertEqual(client_request.data['name'], test_product_name)
        self.assertEqual(str(client_request.data['team_id']), str(self.team_id))
        self.assertTrue('created_at' in client_request.data)
        self.assertTrue('updated_at' in client_request.data)

        # user auth
        user_request = self.client.post(BASE_URL, {
            'name': test_product_name,
            'team_id': self.team_id,
        }, **self.user_auth_headers)
        self.assertTrue('id' in user_request.data)
        self.assertEqual(user_request.data['name'], test_product_name)
        self.assertEqual(str(user_request.data['team_id']), str(self.team_id))
        self.assertTrue('created_at' in user_request.data)
        self.assertTrue('updated_at' in user_request.data)

    def test_post_product_no_name(self):
        """Should return a clean 400 error with helpful text"""
        # client auth
        client_request = self.client.post(BASE_URL, {
            'team_id': self.team_id,
        }, **self.client_auth_headers)
        self.assertContains(client_request, 'name', status_code=400)

        # user auth
        user_request = self.client.post(BASE_URL, {
            'team_id': self.team_id,
        }, **self.user_auth_headers)
        self.assertContains(user_request, 'name', status_code=400)

    def test_post_product_no_team_id(self):
        """Should return a clean 400 error"""
        test_product_name = 'Test Product'

        # client auth
        client_request = self.client.post(BASE_URL, {
            'name': test_product_name,
        }, **self.client_auth_headers)
        self.assertContains(client_request, 'team_id', status_code=400)

        # user auth
        user_request = self.client.post(BASE_URL, {
            'name': test_product_name,
        }, **self.user_auth_headers)
        self.assertContains(user_request, 'team_id', status_code=400)

    def test_post_product_vendor_all_data(self):
        """Should return a 201"""
        # client request
        integrations_id = str(uuid4())
        client_request = self.client.post(f'{BASE_URL}/{self.product.id}/vendors', {
            'name': 'Test Vendor',
            'vendor_product_id': 'abcdef',
            'integrations_type': 'amazon',
            'integrations_id': integrations_id,
        }, **self.client_auth_headers)
        self.assertContains(client_request, 'Test Vendor', status_code=201)
        self.assertContains(client_request, 'amazon', status_code=201)
        self.assertContains(client_request, integrations_id, status_code=201)
        self.assertEqual(client_request.json()['team_id'], self.team_id)

        # user request
        integrations_id = str(uuid4())
        user_request = self.client.post(f'{BASE_URL}/{self.product.id}/vendors', {
            'name': 'Test Vendor',
            'vendor_product_id': 'abcdef',
            'integrations_type': 'amazon',
            'integrations_id': integrations_id,
        }, **self.user_auth_headers)
        self.assertContains(user_request, 'Test Vendor', status_code=201)
        self.assertContains(user_request, 'amazon', status_code=201)
        self.assertContains(user_request, integrations_id, status_code=201)
        self.assertEqual(user_request.json()['team_id'], self.team_id)

    def test_post_product_vendor_without_integrations_type(self):
        """Should return a 201"""
        # client request
        integrations_id     = str(uuid4())
        vendor_product_id   = str(uuid4())
        client_request = self.client.post(f'{BASE_URL}/{self.product.id}/vendors', {
            'name': 'Test Vendor',
            'vendor_product_id': vendor_product_id,
            'integrations_id': integrations_id,
        }, **self.client_auth_headers)
        self.assertContains(client_request, 'Test Vendor', status_code=201)
        self.assertContains(client_request, integrations_id, status_code=201)

        # user request
        integrations_id     = str(uuid4())
        vendor_product_id   = str(uuid4())
        user_request = self.client.post(f'{BASE_URL}/{self.product.id}/vendors', {
            'name': 'Test Vendor',
            'vendor_product_id': vendor_product_id,
            'integrations_id': integrations_id,
        }, **self.user_auth_headers)
        self.assertContains(user_request, 'Test Vendor', status_code=201)
        self.assertContains(user_request, integrations_id, status_code=201)

    def test_post_product_vendor_without_integrations_id(self):
        """Should return a 201"""
        # client request
        vendor_product_id = str(uuid4())
        client_request = self.client.post(f'{BASE_URL}/{self.product.id}/vendors', {
            'name': 'Test Vendor',
            'vendor_product_id': vendor_product_id,
            'integrations_type': 'amazon',
        }, **self.client_auth_headers)
        self.assertContains(client_request, 'Test Vendor', status_code=201)
        self.assertContains(client_request, 'amazon', status_code=201)

        # user request
        vendor_product_id = str(uuid4())
        user_request = self.client.post(f'{BASE_URL}/{self.product.id}/vendors', {
            'name': 'Test Vendor',
            'vendor_product_id': vendor_product_id,
            'integrations_type': 'amazon',
        }, **self.user_auth_headers)
        self.assertContains(user_request, 'Test Vendor', status_code=201)
        self.assertContains(user_request, 'amazon', status_code=201)


    def test_post_product_vendor_without_name(self):
        """Should return a 400 and contain helpful information"""
        # client request
        client_request = self.client.post(f'{BASE_URL}/{self.product.id}/vendors', {
            'vendor_product_id': '3201',
        }, **self.client_auth_headers)
        self.assertContains(client_request, 'name', status_code=400)

    def test_post_product_vendor_without_vendor_product_id(self):
        """Should return a 400 and contain helpful information"""
        request = self.client.post(f'{BASE_URL}/{self.product.id}/vendors', {
            'name': 'Test Vendor',
        }, **self.client_auth_headers)
        self.assertContains(request, 'vendor_product_id', status_code=400)

    def test_post_product_vendor_where_product_doesnt_exist(self):
        """Should return a 400 and contain helpful information"""
        request = self.client.post(f'{BASE_URL}/{uuid4()}/vendors', {
            'name': 'Test Vendor',
            'vendor_product_id': 'abcdef',
        }, **self.client_auth_headers)
        self.assertContains(request, 'product', status_code=400)

    def test_post_product_vendor_without_team_id(self):
        """Should return a 201 and use the product's team id"""
        request = self.client.post(f'{BASE_URL}/{self.product.id}/vendors', {
            'name': 'Test Vendor',
            'vendor_product_id': 'abcdef',
        }, **self.client_auth_headers)
        self.assertContains(request, 'team_id', status_code=201)
        self.assertEqual(request.json()['team_id'], self.product.team_id)
