from django.core.exceptions import ValidationError
from django.test import TestCase

from common.models import Inventory, Product, Transaction, Vendor

class TransactionModelTests(TestCase):
    def setUp(self):
        self.vendor_transaction_id  = '1112222'
        self.customer_email         = 'julie@example.com'
        self.customer_phone         = '2525550000'
        self.product                = Product.objects.create(name='Test Product')
        self.vendor                 = Vendor.objects.create(name='Test Vendor')
        self.inventory              = Inventory.objects.create(product=self.product, vendor=self.vendor, vendor_product_id='1')

    def test_create_transaction_valid(self):
        """Creating a transaction on the happy path works"""
        transaction = Transaction.objects.create(
            vendor=self.vendor,
            vendor_transaction_id=self.vendor_transaction_id,
            customer_email=self.customer_email,
            customer_phone=self.customer_phone,
        )
        transaction.products.add(self.product)
        self.assertIsInstance(transaction, Transaction)
        self.assertIn(self.product, transaction.products.all())

    def test_products_belong_to_vendor(self):
        """Should raise exception if trying to add a transaction with a product that isn't related to the vendor"""
        product2    = Product.objects.create(name='Unrelated Product')
        transaction = Transaction.objects.create(
            vendor=self.vendor,
            vendor_transaction_id=self.vendor_transaction_id,
            customer_email=self.customer_email,
            customer_phone=self.customer_phone,
        )
        with self.assertRaises(ValidationError):
            transaction.products.add(product2)
