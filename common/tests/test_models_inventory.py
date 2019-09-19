from django.db.utils import IntegrityError
from django.test import TestCase

from common.models import Inventory, Product, Vendor

class TransactionModelTests(TestCase):
    def setUp(self):
        self.product        = Product.objects.create(name='Test Product')
        self.vendor         = Vendor.objects.create(name='Test Vendor')

    def test_create_inventory_valid(self):
        """Creating an inventory relationship on the happy path works"""
        inventory = Inventory.objects.create(
            vendor=self.vendor,
            product=self.product,
            vendor_product_id='1',
        )
        self.assertIsInstance(inventory, Inventory)

    def test_create_duplicate_inventory_fails(self):
        """Creating 2 inventory relationships between the same vendor and product fails"""
        inventory1 = Inventory.objects.create(
            vendor=self.vendor,
            product=self.product,
            vendor_product_id='1',
        )
        with self.assertRaises(IntegrityError):
            inventory2 = Inventory.objects.create(
                vendor=self.vendor,
                product=self.product,
                vendor_product_id='2',
            )

    def test_create_duplicate_vendor_product_id_under_same_vendor(self):
        """Creating different product mappings with the same vendor_product_id fails"""
        duplicated_vendor_product_id = '1'
        inventory1 = Inventory.objects.create(
            vendor=self.vendor,
            product=self.product,
            vendor_product_id=duplicated_vendor_product_id,
        )
        product2 = Product.objects.create(name='Second Product')
        with self.assertRaises(IntegrityError):
            inventory2 = Inventory.objects.create(
                vendor=self.vendor,
                product=product2,
                vendor_product_id=duplicated_vendor_product_id,
            )

    def test_create_duplicate_vendor_product_id_under_different_vendors(self):
        """Creating different product mappings with the same vendor_product_id under different vendors succeeds"""
        duplicated_vendor_product_id = '1'
        inventory1 = Inventory.objects.create(
            vendor=self.vendor,
            product=self.product,
            vendor_product_id=duplicated_vendor_product_id,
        )
        vendor2     = Vendor.objects.create(name='Second Vendor')
        inventory2  = Inventory.objects.create(
            vendor=vendor2,
            product=self.product,
            vendor_product_id=duplicated_vendor_product_id,
        )
        self.assertIsInstance(inventory1, Inventory)
        self.assertIsInstance(inventory2, Inventory)
