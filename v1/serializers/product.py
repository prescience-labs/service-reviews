from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.models import Inventory, Product, Vendor

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model               = Product
        fields              = [
            'id',
            'name',
            'created_at',
            'updated_at',
        ]
        read_only_fields    = [
            'id',
            'created_at',
            'updated_at',
        ]

class ProductVendorSerializer(serializers.ModelSerializer):
    vendor_product_id = serializers.CharField()

    class Meta:
        model               = Vendor
        fields              = [
            'id',
            'name',
            'integrations_type',
            'integrations_id',
            'vendor_product_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields    = [
            'id',
            'created_at',
            'updated_at',
        ]

    def save(self):
        product_id  = self.context['product_id'] if self.context['product_id'] else None
        product     = Product.objects.get(pk=product_id)
        vendor      = Vendor.objects.create(
            name=self.validated_data['name'],
            integrations_type=self.validated_data['integrations_type'],
            integrations_id=self.validated_data['integrations_id'],
        )
        inventory   = Inventory.objects.create(vendor=vendor, product=product, vendor_product_id=self.validated_data['vendor_product_id'])
        return vendor

class RetrieveProductVendorSerializer(ProductVendorSerializer):
    vendor_product_id = serializers.SerializerMethodField(help_text=_("A value representing the vendor's ID number for the product."))

    def get_vendor_product_id(self, obj):
        """Returns the vendor_product_id of the product given the vendor from the context.

        This relies on a `product_id` being passed in the context.

        Returns:
            string: The vendor-product identifier
        """
        product_id  = self.context['product_id'] if self.context['product_id'] else None
        item        = Inventory.objects.get(product__id=product_id, vendor=obj)
        return item.vendor_product_id
