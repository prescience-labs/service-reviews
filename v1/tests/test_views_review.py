from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient

from common.models import Inventory, Product, Transaction, Vendor

BASE_URL = '/v1/reviews'
headers  = {
    'HTTP_Authorization': 'Basic ' + settings.AUTH_SERVICE['CLIENT_ID'] + ':' + settings.AUTH_SERVICE['CLIENT_SECRET'],
}

class ReviewListViewTests(TestCase):
    def setUp(self):
        self.client         = APIClient()
        self.vendor         = Vendor.objects.create(name='Test vendor', team_id='abc')
        self.product        = Product.objects.create(name='Test product', team_id='abc')
        self.inventory      = Inventory.objects.create(product=self.product, vendor=self.vendor, vendor_product_id=1)
        self.transaction    = Transaction.objects.create(
            vendor=self.vendor,
            vendor_transaction_id=1,
            customer_email='test@example.com',
        )
        self.transaction.products.add(self.product)

        self.unrelated_vendor       = Vendor.objects.create(name='Test vendor 2', team_id='abc')
        self.unrelated_product      = Product.objects.create(name='Test product 2', team_id='abc')
        self.unrelated_inventory    = Inventory.objects.create(product=self.unrelated_product, vendor=self.unrelated_vendor, vendor_product_id=1)
        self.unrelated_transaction  = Transaction.objects.create(
            vendor=self.unrelated_vendor,
            vendor_transaction_id=1,
            customer_email='test@example.com',
        )
        self.unrelated_transaction.products.add(self.unrelated_product)

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

    def test_create_review(self):
        """Should return a 201"""
        result = self.client.post(BASE_URL, {
            'text': 'This is a really fantastic product.',
            'vendor': self.vendor.id,
            'product': self.product.id,
            'transaction': self.transaction.id,
            'rating': 4,
            'rating_max': 5,
        }, **headers)
        self.assertContains(result, 'This is a really fantastic product.', status_code=201)

    def test_create_review_with_wrong_vendor(self):
        """Should return a 400 and contain helpful text"""
        result = self.client.post(BASE_URL, {
            'text': 'This is a really fantastic product.',
            'vendor': self.unrelated_vendor.id,
            'product': self.product.id,
            'transaction': self.transaction.id,
            'rating': 4,
            'rating_max': 5,
        }, **headers)
        self.assertContains(result, "product", status_code=400)
        self.assertContains(result, "inventory", status_code=400)
