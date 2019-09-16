from django.test import TestCase
from rest_framework.test import APIClient

BASE_URL = '/v1/products'

class ProductViewTests(TestCase):
    def __init__(self, *args, **kwargs):
        self.client = APIClient()
        super().__init__(*args, **kwargs)

    def test_no_products(self):
        """Ensures that an empty response (no data existing) looks as expected"""
        request         = self.client.get(BASE_URL)
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
        })
        self.assertTrue('id' in request.data)
        self.assertEqual(test_product_name, request.data['name'])
        self.assertTrue('created_at' in request.data)
        self.assertTrue('updated_at' in request.data)
