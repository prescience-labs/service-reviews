from uuid import uuid4

from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient

from common.models import Inventory, Product, Transaction, Vendor

BASE_URL = '/v1/transactions'
headers  = {
    'HTTP_Authorization': 'Basic ' + settings.AUTH_SERVICE['CLIENT_ID'] + ':' + settings.AUTH_SERVICE['CLIENT_SECRET'],
}

class TransactionListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_no_transactions(self):
        """Ensures that an empty response (no data existing) looks as expected"""
        request         = self.client.get(BASE_URL, **headers)
        expected_result = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': [],
        }
        self.assertDictEqual(request.data, expected_result)

class UpsertTransactionComprehensiveViewTests(TestCase):
    def setUp(self):
        self.client                     = APIClient()
        self.customer_email             = 'julie@example.com'
        self.customer_phone             = '0000000000'
        self.vendor_integrations_id     = '12345'
        self.vendor_integrations_type   = 'amazon'
        self.vendor_product_id          = uuid4()
        self.vendor_product_id_2        = uuid4()
        self.vendor_name                = 'Test Vendor'
        self.product_name               = 'Test Product'
        self.product_name_2             = 'Test Product 2'
        self.vendor_transaction_id      = '12345'
        self.vendor                     = Vendor.objects.create(name=self.vendor_name,
                                                                integrations_id=self.vendor_integrations_id,
                                                                integrations_type=self.vendor_integrations_type,
                                                                )
        self.product                    = Product.objects.create(name=self.product_name)
        self.inventory                  = Inventory.objects.create(vendor=self.vendor,
                                                                   product=self.product,
                                                                   vendor_product_id=self.vendor_product_id,
                                                                   )
        self.product_2                  = Product.objects.create(name=self.product_name_2)
        self.inventory_2                = Inventory.objects.create(vendor=self.vendor,
                                                                   product=self.product_2,
                                                                   vendor_product_id=self.vendor_product_id_2,
                                                                   )

    def test_post_transaction_comprehensive_with_all_data(self):
        """Should return a 201 Created"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_transaction_id': self.vendor_transaction_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        }, **headers)
        self.assertEqual(request.status_code, 201)

    def test_post_transaction_comprehensive_with_multiple_products(self):
        """Should return a 201 Created"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_transaction_id': self.vendor_transaction_id,
            'vendor_product_ids': [
                self.vendor_product_id,
                self.vendor_product_id_2,
            ],
        }, **headers)
        self.assertEqual(request.status_code, 201)

    def test_post_transaction_comprehensive_without_customer_email(self):
        """Should return a 201 Created"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': '',
            'customer_phone': self.customer_phone,
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_transaction_id': self.vendor_transaction_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        }, **headers)
        self.assertEqual(request.status_code, 201)

    def test_post_transaction_comprehensive_with_invalid_customer_email(self):
        """Should return a 400"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': 'random string that is not random',
            'customer_phone': self.customer_phone,
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_transaction_id': self.vendor_transaction_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        }, **headers)
        self.assertEqual(request.status_code, 400)

    def test_post_transaction_comprehensive_without_customer_phone(self):
        """Should return a 201 Created"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': self.customer_email,
            'customer_phone': '',
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_transaction_id': self.vendor_transaction_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        }, **headers)
        self.assertEqual(request.status_code, 201)

    def test_post_transaction_comprehensive_without_customer_information(self):
        """Should return a 400 and contain relevant and helpful text"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': '',
            'customer_phone': '',
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_transaction_id': self.vendor_transaction_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        }, **headers)
        self.assertContains(request, 'customer_email', status_code=400)
        self.assertContains(request, 'customer_phone', status_code=400)

    def test_post_transaction_comprehensive_without_vendor_integrations_type(self):
        """Should return a 400 and contain relevant and helpful text"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            # 'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_transaction_id': self.vendor_transaction_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        }, **headers)
        self.assertContains(request, 'vendor_integrations_type', status_code=400)

    def test_post_transaction_comprehensive_without_vendor_integrations_id(self):
        """Should return a 400 and contain relevant and helpful text"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'vendor_integrations_type': self.vendor_integrations_type,
            # 'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_transaction_id': self.vendor_transaction_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        }, **headers)
        self.assertContains(request, 'vendor_integrations_id', status_code=400)

    def test_post_transaction_comprehensive_without_vendor_product_ids(self):
        """Should return a 400 and contain relevant and helpful text"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_transaction_id': self.vendor_transaction_id,
            # 'vendor_product_ids': [
            #     self.vendor_product_id,
            # ],
        }, **headers)
        self.assertContains(request, 'vendor_product_ids', status_code=400)

    def test_post_transaction_comprehensive_with_invalid_vendor_integrations_type(self):
        """Should return a 400 and contain relevant and helpful text"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'vendor_integrations_type': 'invalid_type',
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_transaction_id': self.vendor_transaction_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        }, **headers)
        self.assertContains(request, 'integrations_type', status_code=400)

    def test_post_transaction_comprehensive_with_invalid_vendor_integrations_id(self):
        """Should return a 400 and contain relevant and helpful text"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': 'invalid_id',
            'vendor_transaction_id': self.vendor_transaction_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        }, **headers)
        self.assertContains(request, 'integrations_id', status_code=400)

    def test_post_transaction_comprehensive_with_invalid_vendor_product_ids(self):
        """Should return a 400 and contain relevant and helpful text"""
        request = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_transaction_id': self.vendor_transaction_id,
            'vendor_product_ids': [
                'invalid_product_id_1',
                'invalid_product_id_2',
            ],
        }, **headers)
        self.assertContains(request, 'vendor_product_id', status_code=400)

    def test_post_transaction_fails_when_vendor_doesnt_have_product_in_inventory(self):
        """Should return a 400 and contain relevant and helpful text"""
        product_name        = 'Unrelated Product'
        unrelated_product   = Product.objects.create(name=product_name)
        request             = self.client.post(BASE_URL, {
            'vendor_transaction_id': self.vendor_transaction_id,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'vendor': self.vendor.id,
            'products': [
                unrelated_product.id,
            ],
        }, **headers)
        self.assertContains(request, self.vendor.name, status_code=400)
        self.assertContains(request, product_name, status_code=400)

    def test_post_transaction_comprehensive_twice_with_same_transaction(self):
        """Should return a 201"""
        transaction_count_init = Transaction.objects.count()
        request1 = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_transaction_id': self.vendor_transaction_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        }, **headers)
        transaction_count_after_one_post = Transaction.objects.count()
        request2 = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_transaction_id': self.vendor_transaction_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        }, **headers)
        transaction_count_after_two_posts = Transaction.objects.count()
        self.assertContains(request1, self.customer_email, status_code=201)
        self.assertContains(request2, self.customer_email, status_code=200)
        self.assertEqual(transaction_count_after_one_post, transaction_count_init + 1)
        self.assertEqual(transaction_count_after_two_posts, transaction_count_after_one_post)

    def test_post_transaction_comprehensive_twice_with_changed_phone_numbers(self):
        """Should return a 201 then a 200"""
        transaction_count_init = Transaction.objects.count()
        request1 = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_transaction_id': self.vendor_transaction_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        }, **headers)
        transaction_count_after_one_post = Transaction.objects.count()
        request2 = self.client.post(BASE_URL + '/comprehensive', {
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone + '1',
            'vendor_integrations_type': self.vendor_integrations_type,
            'vendor_integrations_id': self.vendor_integrations_id,
            'vendor_transaction_id': self.vendor_transaction_id,
            'vendor_product_ids': [
                self.vendor_product_id,
            ],
        }, **headers)
        transaction_count_after_two_posts = Transaction.objects.count()
        self.assertContains(request1, self.customer_email, status_code=201)
        self.assertContains(request2, self.customer_email, status_code=200)
        self.assertEqual(transaction_count_after_one_post, transaction_count_init + 1)
        self.assertEqual(transaction_count_after_two_posts, transaction_count_after_one_post)
