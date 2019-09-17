from uuid import uuid4

from django.test import TestCase
from rest_framework.test import APIClient

from common.models import Inventory, Product, Vendor

BASE_URL = '/v1/transactions'

class TransactionListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_no_transactions(self):
        """Ensures that an empty response (no data existing) looks as expected"""
        request         = self.client.get(BASE_URL)
        expected_result = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': [],
        }
        self.assertDictEqual(request.data, expected_result)

class CreateTransactionComprehensiveViewTests(TestCase):
    def setUp(self):
        self.client                     = APIClient()
        self.customer_email             = 'julie@example.com'
        self.customer_phone             = '0000000000'
        self.vendor_integrations_id     = '12345'
        self.vendor_integrations_type   = 'amazon'
        self.vendor_product_id          = uuid4()
        self.vendor_name                = 'Test Vendor'
        self.product_name               = 'Test Product'
        self.vendor                     = Vendor.objects.create(name=self.vendor_name,
                                                                integrations_id=self.vendor_integrations_id,
                                                                integrations_type=self.vendor_integrations_type,
                                                                )
        self.product                    = Product.objects.create(name=self.product_name)
        self.inventory                  = Inventory.objects.create(vendor=self.vendor,
                                                                   product=self.product,
                                                                   vendor_product_id=self.vendor_product_id,
                                                                   )

    def test_post_transaction_comprehensive_with_all_data(self):
        """Should return a 201 Created"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        })
        self.assertEqual(request.status_code, 201)

    def test_post_transaction_comprehensive_without_customer_email(self):
        """Should return a 201 Created"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': '',
            'customer_phone': self.customer_phone,
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        })
        self.assertEqual(request.status_code, 201)

    def test_post_transaction_comprehensive_with_invalid_customer_email(self):
        """Should return a 400"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': 'random string that is not random',
            'customer_phone': self.customer_phone,
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        })
        self.assertEqual(request.status_code, 400)

    def test_post_transaction_comprehensive_without_customer_phone(self):
        """Should return a 201 Created"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': self.customer_email,
            'customer_phone': '',
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        })
        self.assertEqual(request.status_code, 201)

    def test_post_transaction_comprehensive_without_customer_information(self):
        """Should return a 400"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': '',
            'customer_phone': '',
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        })
        self.assertEqual(request.status_code, 400)
