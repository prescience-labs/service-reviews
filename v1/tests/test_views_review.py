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
        self.vendor         = Vendor.objects.create(name='Test vendor')
        self.product        = Product.objects.create(name='Test product')
        self.inventory      = Inventory.objects.create(product=self.product, vendor=self.vendor, vendor_product_id=1)
        self.transaction    = Transaction.objects.create(
            vendor=self.vendor,
            vendor_transaction_id=1,
            customer_email='test@example.com',
        )
        self.transaction.products.add(self.product)

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
