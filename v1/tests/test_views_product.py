from uuid import uuid4

from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient

from common.models import Inventory, Product, Vendor

BASE_URL = '/v1/products'
headers  = {
    'HTTP_Authorization': 'Basic ' + settings.AUTH_SERVICE['CLIENT_ID'] + ':' + settings.AUTH_SERVICE['CLIENT_SECRET'],
}

class ProductListViewTests(TestCase):
    def setUp(self):
        self.client     = APIClient()
        self.team_id    = str(uuid4())
        self.product    = Product.objects.create(name='Test Product', team_id=self.team_id)

    def test_no_products(self):
        """Ensures that an empty response (no data existing) looks as expected"""
        self.product.delete()
        request         = self.client.get(BASE_URL, **headers)
        expected_result = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': [],
        }
        self.assertDictEqual(request.data, expected_result)

    def test_post_product(self):
        """Should add a product and return product data"""
        test_product_name = 'Test Product 1'
        request = self.client.post(BASE_URL, {
            'name': test_product_name,
            'team_id': self.team_id,
        }, **headers)
        self.assertTrue('id' in request.data)
        self.assertEqual(request.data['name'], test_product_name)
        self.assertEqual(str(request.data['team_id']), str(self.team_id))
        self.assertTrue('created_at' in request.data)
        self.assertTrue('updated_at' in request.data)

    def test_post_product_no_name(self):
        """Should return a clean 400 error with helpful text"""
        request = self.client.post(BASE_URL, {
            'team_id': self.team_id,
        }, **headers)
        self.assertContains(request, 'name', status_code=400)

    def test_post_product_no_team_id(self):
        """Should return a clean 400 error"""
        test_product_name = 'Test Product'
        request = self.client.post(BASE_URL, {
            'name': test_product_name,
        }, **headers)
        self.assertContains(request, 'team_id', status_code=400)

    def test_post_product_vendor_all_data(self):
        """Should return a 201"""
        request = self.client.post(f'{BASE_URL}/{self.product.id}/vendors', {
            'name': 'Test Vendor',
            'vendor_product_id': 'abcdef',
            'integrations_type': 'amazon',
            'integrations_id': '1772661',
        }, **headers)
        self.assertContains(request, 'Test Vendor', status_code=201)
        self.assertContains(request, 'amazon', status_code=201)
        self.assertContains(request, '1772661', status_code=201)
        self.assertEqual(request.json()['team_id'], self.team_id)

    def test_post_product_vendor_without_integrations_type(self):
        """Should return a 201"""
        request = self.client.post(f'{BASE_URL}/{self.product.id}/vendors', {
            'name': 'Test Vendor',
            'vendor_product_id': 'abcdef',
            'integrations_id': '1772661',
        }, **headers)
        self.assertContains(request, 'Test Vendor', status_code=201)
        self.assertContains(request, '1772661', status_code=201)

    def test_post_product_vendor_without_integrations_id(self):
        """Should return a 201"""
        request = self.client.post(f'{BASE_URL}/{self.product.id}/vendors', {
            'name': 'Test Vendor',
            'vendor_product_id': 'abcdef',
            'integrations_type': 'amazon',
        }, **headers)
        self.assertContains(request, 'Test Vendor', status_code=201)
        self.assertContains(request, 'amazon', status_code=201)

    def test_post_product_vendor_without_name(self):
        """Should return a 400 and contain helpful information"""
        request = self.client.post(f'{BASE_URL}/{self.product.id}/vendors', {
            'vendor_product_id': '3201',
        }, **headers)
        self.assertContains(request, 'name', status_code=400)

    def test_post_product_vendor_without_vendor_product_id(self):
        """Should return a 400 and contain helpful information"""
        request = self.client.post(f'{BASE_URL}/{self.product.id}/vendors', {
            'name': 'Test Vendor',
        }, **headers)
        self.assertContains(request, 'vendor_product_id', status_code=400)

    def test_post_product_vendor_where_product_doesnt_exist(self):
        """Should return a 400 and contain helpful information"""
        request = self.client.post(f'{BASE_URL}/{uuid4()}/vendors', {
            'name': 'Test Vendor',
            'vendor_product_id': 'abcdef',
        }, **headers)
        self.assertContains(request, 'product', status_code=400)

    def test_post_product_vendor_without_team_id(self):
        """Should return a 201 and use the product's team id"""
        request = self.client.post(f'{BASE_URL}/{self.product.id}/vendors', {
            'name': 'Test Vendor',
            'vendor_product_id': 'abcdef',
        }, **headers)
        self.assertContains(request, 'team_id', status_code=201)
        self.assertEqual(request.json()['team_id'], self.product.team_id)
